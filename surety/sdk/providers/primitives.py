import random
import string

from faker.providers import BaseProvider


class PrimitivesProvider(BaseProvider):
    def string(self, min_chars=1, max_chars=20):
        length = random.randint(min_chars, max_chars)
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def number(self, min_value=0, max_value=9999):
        return random.randint(min_value, max_value)
