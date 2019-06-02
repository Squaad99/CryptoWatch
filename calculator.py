
class Calculator:

    @staticmethod
    def percentage_of_two_values(first_value, second_value):
        total = first_value + second_value
        return round((first_value/total * 100), 2), round((second_value/total * 100), 2)

