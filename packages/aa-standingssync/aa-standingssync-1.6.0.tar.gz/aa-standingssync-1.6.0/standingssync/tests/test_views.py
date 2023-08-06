from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse
from esi.models import Token

from allianceauth.authentication.models import CharacterOwnership
from allianceauth.eveonline.models import EveCharacter
from app_utils.testing import NoSocketsTestCase, create_user_from_evecharacter

from .. import views
from ..models import EveEntity, SyncedCharacter, SyncManager
from .factories import EveContactFactory, SyncedCharacterFactory, SyncManagerFactory
from .utils import ALLIANCE_CONTACTS, LoadTestDataMixin

MODULE_PATH = "standingssync.views"


class TestMainScreen(LoadTestDataMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # user 1 is the manager
        cls.user_1, _ = create_user_from_evecharacter(cls.character_1.character_id)
        # sync manager with contacts
        cls.sync_manager = SyncManagerFactory(user=cls.user_1, version_hash="new")
        for contact in ALLIANCE_CONTACTS:
            EveContactFactory(
                manager=cls.sync_manager,
                eve_entity=EveEntity.objects.get(id=contact["contact_id"]),
                standing=contact["standing"],
            )

        # user 2 is a normal user and has two alts and permission
        cls.user_2, _ = create_user_from_evecharacter(
            cls.character_2.character_id,
            permissions=["standingssync.add_syncedcharacter"],
        )
        cls.alt_ownership_1 = CharacterOwnership.objects.create(
            character=cls.character_4, owner_hash="x4", user=cls.user_2
        )
        cls.user_2 = User.objects.get(pk=cls.user_2.pk)
        cls.sync_char = SyncedCharacterFactory(
            manager=cls.sync_manager, character_ownership=cls.alt_ownership_1
        )

        # user 3 has no permission
        cls.user_3, _ = create_user_from_evecharacter(cls.character_3.character_id)
        cls.factory = RequestFactory()

    def test_user_with_permission_can_open_app(self):
        request = self.factory.get(reverse("standingssync:index"))
        request.user = self.user_2
        response = views.index(request)
        self.assertEqual(response.status_code, 200)

    def test_user_wo_permission_can_not_open_app(self):
        request = self.factory.get(reverse("standingssync:index"))
        request.user = self.user_3
        response = views.index(request)
        self.assertEqual(response.status_code, 302)

    @patch(MODULE_PATH + ".messages_plus")
    def test_user_can_remove_sync_char(self, mock_messages_plus):
        request = self.factory.get(
            reverse("standingssync:remove_character", args=(self.sync_char.pk,))
        )
        request.user = self.user_2
        response = views.remove_character(request, self.sync_char.pk)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(mock_messages_plus.success.called)
        self.assertFalse(SyncedCharacter.objects.filter(pk=self.sync_char.pk).exists())

    def test_user_with_permission_can_set_alliance_char(self):
        pass

    def test_user_wo_permission_can_not_set_alliance_char(self):
        pass


@patch(MODULE_PATH + ".tasks.run_character_sync")
@patch(MODULE_PATH + ".messages_plus")
class TestAddSyncChar(LoadTestDataMixin, NoSocketsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # user 1 is the manager
        cls.user_1, _ = create_user_from_evecharacter(
            cls.character_1.character_id, permissions=["standingssync.add_syncmanager"]
        )
        # sync manager with contacts
        cls.sync_manager = SyncManagerFactory(user=cls.user_1, version_hash="new")
        for contact in ALLIANCE_CONTACTS:
            EveContactFactory(
                manager=cls.sync_manager,
                eve_entity=EveEntity.objects.get(id=contact["contact_id"]),
                standing=contact["standing"],
            )

        # user 2 is a normal user and has three alts
        cls.user_2, _ = create_user_from_evecharacter(
            cls.character_2.character_id,
            permissions=["standingssync.add_syncedcharacter"],
        )
        cls.alt_ownership_1 = CharacterOwnership.objects.create(
            character=cls.character_4, owner_hash="x4", user=cls.user_2
        )
        cls.alt_ownership_2 = CharacterOwnership.objects.create(
            character=cls.character_5, owner_hash="x5", user=cls.user_2
        )
        CharacterOwnership.objects.create(
            character=cls.character_6, owner_hash="x6", user=cls.user_2
        )
        cls.factory = RequestFactory()

    def make_request(self, user, character):
        token = Mock(spec=Token)
        token.character_id = character.character_id
        request = self.factory.get(reverse("standingssync:add_character"))
        request.user = user
        request.token = token
        middleware = SessionMiddleware(Mock())
        middleware.process_request(request)
        orig_view = views.add_character.__wrapped__.__wrapped__.__wrapped__
        return orig_view(request, token)

    def test_users_can_not_add_alliance_members(
        self, mock_messages_plus, mock_run_character_sync
    ):
        response = self.make_request(self.user_2, self.character_2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("standingssync:index"))
        self.assertTrue(mock_messages_plus.warning.called)
        self.assertFalse(mock_run_character_sync.delay.called)

    def test_user_can_add_blue_alt(self, mock_messages_plus, mock_run_character_sync):
        response = self.make_request(self.user_2, self.character_4)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("standingssync:index"))
        self.assertTrue(mock_messages_plus.success.called)
        self.assertTrue(mock_run_character_sync.delay.called)
        self.assertTrue(
            SyncedCharacter.objects.filter(manager=self.sync_manager)
            .filter(character_ownership__character=self.character_4)
            .exists()
        )

    @patch(MODULE_PATH + ".STANDINGSSYNC_CHAR_MIN_STANDING", 0)
    def test_user_can_add_neutral_alt(
        self, mock_messages_plus, mock_run_character_sync
    ):
        response = self.make_request(self.user_2, self.character_6)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("standingssync:index"))
        self.assertTrue(mock_messages_plus.success.called)
        self.assertTrue(mock_run_character_sync.delay.called)
        self.assertTrue(
            SyncedCharacter.objects.filter(manager=self.sync_manager)
            .filter(character_ownership__character=self.character_6)
            .exists()
        )

    def test_user_can_not_add_non_blue_alt(
        self, mock_messages_plus, mock_run_character_sync
    ):
        response = self.make_request(self.user_2, self.character_5)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("standingssync:index"))
        self.assertTrue(mock_messages_plus.warning.called)
        self.assertFalse(mock_run_character_sync.delay.called)
        self.assertFalse(
            SyncedCharacter.objects.filter(manager=self.sync_manager)
            .filter(character_ownership__character=self.character_5)
            .exists()
        )

    def test_user_can_not_add_char_users_down_not_own(
        self, mock_messages_plus, mock_run_character_sync
    ):
        response = self.make_request(self.user_2, self.character_3)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("standingssync:index"))
        self.assertTrue(mock_messages_plus.warning.called)
        self.assertFalse(mock_run_character_sync.delay.called)
        self.assertFalse(
            SyncedCharacter.objects.filter(manager=self.sync_manager)
            .filter(character_ownership__character=self.character_3)
            .exists()
        )

    def test_raises_exception_if_alliance_not_found(
        self, mock_messages_plus, mock_run_character_sync
    ):
        my_char = EveCharacter.objects.create(
            character_id=1098,
            character_name="Joker",
            corporation_id=2098,
            corporation_name="Joker Corp",
            alliance_id=3098,
            alliance_name="Joker Alliance",
        )
        my_user, _ = create_user_from_evecharacter(my_char.character_id)
        with self.assertRaises(RuntimeError):
            self.make_request(my_user, self.character_4)

    def test_raises_exception_if_no_sync_manager_for_alliance(
        self, mock_messages_plus, mock_run_character_sync
    ):
        my_user, _ = create_user_from_evecharacter(self.character_3.character_id)
        with self.assertRaises(RuntimeError):
            self.make_request(my_user, self.character_4)


@patch(MODULE_PATH + ".tasks.run_manager_sync")
@patch(MODULE_PATH + ".messages_plus")
class TestAddAllianceManager(LoadTestDataMixin, NoSocketsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # user 1 is the manager
        cls.user_1, _ = create_user_from_evecharacter(
            cls.character_1.character_id,
            permissions=[
                "standingssync.add_syncmanager",
                "standingssync.add_syncedcharacter",
            ],
        )
        # sync manager with contacts
        cls.sync_manager = SyncManagerFactory(user=cls.user_1, version_hash="new")
        for contact in ALLIANCE_CONTACTS:
            EveContactFactory(
                manager=cls.sync_manager,
                eve_entity=EveEntity.objects.get(id=contact["contact_id"]),
                standing=contact["standing"],
            )

        # user 2 is a normal user and has two alts
        cls.user_2, _ = create_user_from_evecharacter(
            cls.character_2.character_id,
            permissions=["standingssync.add_syncedcharacter"],
        )
        cls.alt_ownership_1 = CharacterOwnership.objects.create(
            character=cls.character_4, owner_hash="x4", user=cls.user_2
        )
        cls.alt_ownership_2 = CharacterOwnership.objects.create(
            character=cls.character_5, owner_hash="x5", user=cls.user_2
        )
        cls.factory = RequestFactory()

    def make_request(self, user, character):
        token = Mock(spec=Token)
        token.character_id = character.character_id
        request = self.factory.get(reverse("standingssync:add_alliance_manager"))
        request.user = user
        request.token = token
        middleware = SessionMiddleware(Mock())
        middleware.process_request(request)
        orig_view = views.add_alliance_manager.__wrapped__.__wrapped__.__wrapped__
        return orig_view(request, token)

    def test_user_with_permission_can_add_alliance_manager(
        self, mock_messages_plus, mock_run_manager_sync
    ):
        response = self.make_request(self.user_1, self.character_1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("standingssync:index"))
        self.assertTrue(mock_messages_plus.success.called)
        self.assertTrue(mock_run_manager_sync.delay.called)
        self.assertTrue(
            SyncManager.objects.filter(alliance=self.alliance_1)
            .filter(character_ownership__character=self.character_1)
            .exists()
        )

    """
    def test_user_wo_permission_can_not_add_alliance_manager(
        self, mock_messages_plus, mock_run_manager_sync
    ):
        response = self.make_request(self.user_2, self.character_2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('standingssync:index'))
        self.assertFalse(mock_run_manager_sync.delay.called)
        self.assertFalse(
            SyncManager.objects
            .filter(alliance=self.alliance_1)
            .filter(character_ownership__character=self.character_2)
            .exists()
        )
    """

    def test_character_for_manager_must_be_alliance_member(
        self, mock_messages_plus, mock_run_manager_sync
    ):
        response = self.make_request(self.user_1, self.character_5)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("standingssync:index"))
        self.assertTrue(mock_messages_plus.warning.called)
        self.assertFalse(mock_run_manager_sync.delay.called)
        self.assertFalse(
            SyncManager.objects.filter(alliance=self.alliance_1)
            .filter(character_ownership__character=self.character_5)
            .exists()
        )

    def test_character_for_manager_must_be_owned_by_user(
        self, mock_messages_plus, mock_run_manager_sync
    ):
        response = self.make_request(self.user_1, self.character_3)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("standingssync:index"))
        self.assertTrue(mock_messages_plus.warning.called)
        self.assertFalse(mock_run_manager_sync.delay.called)
        self.assertFalse(
            SyncManager.objects.filter(alliance=self.alliance_1)
            .filter(character_ownership__character=self.character_3)
            .exists()
        )
