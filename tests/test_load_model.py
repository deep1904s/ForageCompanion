import os
import unittest
from tensorflow import keras

MODEL_PATH = os.path.join("models", "mushroom_classifierV2.keras")


class TestModelLoading(unittest.TestCase):
    def test_model_can_load(self):
        """Test that the Keras model can be loaded without errors."""
        try:
            model = keras.models.load_model(MODEL_PATH)
            self.assertIsNotNone(model)
        except Exception as e:
            self.fail(f"Model failed to load with error: {e}")


if __name__ == "__main__":
    unittest.main()
