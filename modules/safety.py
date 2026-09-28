class HealthSafetyEngine:

    DISCLAIMER = (
        "SmartHealth AI provides model-generated "
        "possibilities and general wellness information. "
        "It is not a medical diagnosis and should not "
        "replace advice from a qualified healthcare "
        "professional."
    )

    TRADITIONAL_DISCLAIMER = (
        "Ayurvedic and homeopathic information shown "
        "by this application is provided for traditional "
        "and educational reference only. It should not "
        "be interpreted as a proven treatment or a "
        "substitute for professional medical care."
    )

    @classmethod
    def get_disclaimer(cls):

        return cls.DISCLAIMER

    @classmethod
    def get_traditional_disclaimer(cls):

        return cls.TRADITIONAL_DISCLAIMER

    @staticmethod
    def validate_age(age):

        try:

            age = int(age)

        except (
            ValueError,
            TypeError
        ):

            return False

        return 1 <= age <= 120

    @staticmethod
    def validate_weight(weight):

        try:

            weight = float(weight)

        except (
            ValueError,
            TypeError
        ):

            return False

        return 1 <= weight <= 500

    @staticmethod
    def validate_height(height):

        try:

            height = float(height)

        except (
            ValueError,
            TypeError
        ):

            return False

        return 30 <= height <= 250

    @staticmethod
    def emergency_warning():

        return (
            "If you are experiencing severe or "
            "rapidly worsening symptoms, seek "
            "appropriate emergency medical care "
            "instead of relying on this application."
        )