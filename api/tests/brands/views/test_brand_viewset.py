from brands.models import Brand
from django.urls import reverse
from tests.setup.mixins.create_user_mixin import CreateUserMixin
from tests.setup.mixins.request_mixin import RequestMixin


class TestBrandViewSet(RequestMixin, CreateUserMixin):
    def test_list_blocks_non_authenticated_users_on_lookup(self):
        brand_id = Brand.objects.all().values_list("id", flat=True).first()
        response = self.public_client.get(path=reverse("brands:brands-detail", args=(brand_id,)))
        self.assertEqual(response.status_code, 403)

    def test_list_blocks_non_authenticated_users_on_list(self):
        response = self.public_client.get(path=reverse("brands:brands-list"))
        self.assertEqual(response.status_code, 403)

    def test_allows_authenticated_user_on_lookup(self):
        client = self.login(self.user)
        brand_id = Brand.objects.all().values_list("id", flat=True).first()
        response = self.get(client, path=reverse("brands:brands-detail", args=(brand_id,)))
        self.assertEqual(response.status_code, 200)

    def test_allows_authenticated_user_on_list(self):
        client = self.login(self.user)
        response = self.get(client, path=reverse("brands:brands-list"))
        self.assertEqual(response.status_code, 200)

    def test_blocks_creation_methods(self):
        client = self.login(self.user)
        response = self.post(client, path=reverse("brands:brands-list"), data={}, content_type="application/json")
        self.assertEqual(response.status_code, 405)

    def test_blocks_updating_methods(self):
        client = self.login(self.user)
        brand_id = Brand.objects.all().values_list("id", flat=True).first()
        response = self.put(
            client, path=reverse("brands:brands-detail", args=(brand_id,)), data={}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 405)

    def test_blocks_deletion_methods(self):
        client = self.login(self.user)
        brand_id = Brand.objects.all().values_list("id", flat=True).first()
        response = self.delete(
            client, path=reverse("brands:brands-detail", args=(brand_id,)), content_type="application/json"
        )
        self.assertEqual(response.status_code, 405)

    def test_serializes_response_properly_on_lookup(self):
        client = self.login(self.user)
        brand_id = Brand.objects.all().values_list("id", flat=True).first()
        response = self.get(client, path=reverse("brands:brands-detail", args=(brand_id,)))
        self.assertEqual(response.status_code, 200)
        self._assert_response_contains_correct_keys(response.json())

    def test_serializes_response_properly_on_list(self):
        client = self.login(self.user)
        response = self.get(client, path=reverse("brands:brands-list"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for brand in data:
            self._assert_response_contains_correct_keys(brand)
        self.assertGreater(len(data), 0)

    def test_under_armour_enabled(self):
        client = self.login(self.user)
        under_armour = Brand.objects.get(name="Under Armour")
        self.assertTrue(under_armour.enabled)
        response = self.get(client, path=reverse("brands:brands-detail", args=(under_armour.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self._assert_response_contains_correct_keys(data)
        self.assertTrue(data["enabled"])

    def test_north_face_enabled(self):
        client = self.login(self.user)
        north_face = Brand.objects.get(name="North Face")
        self.assertTrue(north_face.enabled)
        response = self.get(client, path=reverse("brands:brands-detail", args=(north_face.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self._assert_response_contains_correct_keys(data)
        self.assertTrue(data["enabled"])

    def test_new_balance_enabled(self):
        client = self.login(self.user)
        new_balance = Brand.objects.get(name="New Balance")
        self.assertTrue(new_balance.enabled)
        response = self.get(client, path=reverse("brands:brands-detail", args=(new_balance.id,)))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self._assert_response_contains_correct_keys(data)
        self.assertTrue(data["enabled"])

    def _assert_response_contains_correct_keys(self, response: dict):
        self.assertTrue("id" in response)
        self.assertTrue("name" in response)
        self.assertTrue("created_at" in response)
        self.assertTrue("updated_at" in response)
        self.assertTrue("logo" in response)
        self.assertTrue("enabled" in response)
        self.assertTrue("pkid" not in response)
