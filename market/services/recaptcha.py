from httpx import Client, RequestError


class RecaptchaV2:
    @staticmethod
    def verify_recaptcha(response: str, secret_key: str) -> bool:
        try:
            with Client() as client:
                resp = client.post(
                    "https://www.google.com/recaptcha/api/siteverify",
                    data={
                        "secret": secret_key,
                        "response": response,
                    }
                )

                return resp.json().get("success", False)

        except RequestError:
            return False
