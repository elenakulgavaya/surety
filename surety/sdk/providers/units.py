from faker.providers import BaseProvider

_UNITS = [
    ('Bottle', 'BOT'),
    ('Box', 'BOX'),
    ('Can', 'CAN'),
    ('Case', 'CS'),
    ('Feet', 'FT'),
    ('Gallon', 'GA'),
    ('Gram', 'GR'),
    ('Inches', 'IN'),
    ('Kilogram', 'KG'),
    ('Pounds', 'LB'),
    ('Liter', 'LTR'),
    ('Milliliter', 'ML'),
    ('Millimeter', 'MM'),
    ('Meter', 'MTR'),
    ('Ounces', 'OZ'),
    ('Pieces', 'PCS'),
]


class UnitsProvider(BaseProvider):
    def unit(self):
        return self.random_element(_UNITS)[0]

    def unit_code(self):
        return self.random_element(_UNITS)[1]
