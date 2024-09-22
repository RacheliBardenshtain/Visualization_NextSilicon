import unittest
from entities.component import Component

class TestComponent(unittest.TestCase):

    def test_component_auto_id(self):
        component1 = Component(type_name="test")
        component2 = Component(type_name="test")
        self.assertEqual(component2.id, component1.id + 1)

    def test_component_custom_id(self):
        component = Component(id=5, type_name="test")
        self.assertEqual(component.id, 5)

# if __name__ == '__main__':
#     unittest.main()
