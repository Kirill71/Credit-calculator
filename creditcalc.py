import argparse
import math


class CreditCalculator:
    __months_per_year = 12

    def __init__(self):
        self.__principal = 0
        self.__month_payment = 0
        self.__credit_interest = 0.0
        self.__periods = 0

    def set_principal(self, principal):
        self.__principal = principal
        return self

    def set_payment(self, payment):
        self.__month_payment = payment
        return self

    def set_interest(self, credit):
        self.__credit_interest = credit
        return self

    def set_periods(self, periods):
        self.__periods = periods
        return self

    def calculate(self, strategy):
        interest_rate = 0.01 * self.__credit_interest / self.__months_per_year
        principal = self.__principal
        periods = self.__periods
        payment = self.__month_payment

        if strategy == 'annuity':
            if principal > 0 and payment > 0 and interest_rate > 0:
                self.__calculate_count_of_month(interest_rate)
            elif principal > 0 and periods > 0 and interest_rate > 0:
                self.__calculate_annuity(interest_rate)
            elif payment > 0 and periods > 0 and interest_rate > 0:
                self.__calculate_principal(interest_rate)
            else:
                print('Incorrect parameters.')
        elif strategy == 'diff' and  principal > 0 and periods > 0 and interest_rate > 0:
            self.__calculate_differentiated_payments(interest_rate)
        else:
            print('Incorrect parameters.')

    def __calculate_count_of_month(self, interest_rate):
        month_payment = self.__month_payment
        principal = self.__principal
        periods = math.ceil(math.log(month_payment / (month_payment - interest_rate * principal), 1 + interest_rate))
        self.__prepare_periods(periods)
        print(f'Overpayment = {math.ceil(periods * month_payment - principal)}')

    def __calculate_annuity(self, interest_rate):
        principal = self.__principal
        periods = self.__periods
        month_payment = math.ceil(principal * ((interest_rate * math.pow((1 + interest_rate), periods)) / (
                math.pow((1 + interest_rate), periods) - 1)))
        print(f'Your annuity payment = {month_payment}!')
        self.__calculate_overpayment(periods * month_payment, principal)

    def __calculate_principal(self, interest_rate):
        periods = self.__periods
        month_payment = self.__month_payment
        principal = month_payment / (interest_rate * (math.pow((1. + interest_rate), periods)) / (
                (math.pow(1. + interest_rate, periods)) - 1.))
        print(f'Your credit principal = {math.floor(principal)}!')
        self.__calculate_overpayment(periods * month_payment, principal)

    def __calculate_differentiated_payments(self, interest_rate):
        principal = self.__principal
        periods = self.__periods
        payment = 0
        for i in range(periods):
            month_payment = math.ceil(principal / periods + interest_rate * (principal - (principal * i) / periods))
            payment += month_payment
            print(f'Month {i + 1}: paid out {month_payment}')

        self.__calculate_overpayment(payment, principal)

    @staticmethod
    def __calculate_overpayment(real_payment, credit_principal):
        print(f'Overpayment = {math.ceil(real_payment - credit_principal)}')

    @staticmethod
    def __prepare_periods(periods):
        months_per_year = CreditCalculator.__months_per_year
        month = 1
        if periods < months_per_year:
            s = 's' if periods > month else ''
            print(f'It takes {periods} month{s} to repay the credit')
        else:
            y_s = '' if months_per_year < periods < 2 * months_per_year else 's'
            if periods % months_per_year == 0:
                print(f'It takes  {periods // months_per_year} year{y_s} to repay the credit')
            else:
                s = 's' if periods > month else ''
                print(f'It takes {periods // months_per_year} year{y_s} and {periods % months_per_year} month{s} to '
                      f'repay the credit')


def prepare_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type",
                        action="store", choices=['annuity', 'diff'], required=True)
    parser.add_argument('--principal', type=int, default=0)
    parser.add_argument('--payment', type=int, default=0)
    parser.add_argument('--periods', type=int, default=0)
    parser.add_argument('--interest', type=float, default=0.0, required=True)
    return parser.parse_args()


def main():
    args = prepare_args()
    calculator = CreditCalculator()
    calculator \
        .set_principal(args.principal) \
        .set_periods(abs(args.periods)) \
        .set_interest(args.interest) \
        .set_payment(args.payment) \
        .calculate(args.type)


if __name__ == '__main__':
    main()
