from faker.providers import BaseProvider


class NutritionProvider(BaseProvider):
    def calories(self):
        return f'{self.random_int(0, 900)} kcal'

    def fat(self):
        return f'{round(self.random_int(0, 1000) / 10, 1)} g'

    def saturated_fat(self):
        return f'{round(self.random_int(0, 300) / 10, 1)} g'

    def protein(self):
        return f'{round(self.random_int(0, 500) / 10, 1)} g'

    def sodium(self):
        return f'{self.random_int(0, 2300)} mg'

    def carbohydrates(self):
        return f'{round(self.random_int(0, 3000) / 10, 1)} g'

    def sugar(self):
        return f'{round(self.random_int(0, 1000) / 10, 1)} g'

    def salt(self):
        return f'{round(self.random_int(0, 60) / 10, 1)} g'

    def cholesterol(self):
        return f'{self.random_int(0, 300)} mg'

    def fiber(self):
        return f'{round(self.random_int(0, 300) / 10, 1)} g'
