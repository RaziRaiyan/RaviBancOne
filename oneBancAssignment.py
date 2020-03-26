from money import Money
from decimal import Decimal
from forex_python.converter import CurrencyRates
import csv

with open('HDFC-Input-Case1.csv', 'r') as csv_file:
    csv_header_reader = csv.reader(csv_file)
    csv_file_reader = csv.reader(csv_file)
    next(csv_header_reader)
    dateIndex = None
    debitIndex = None
    creditIndex = None
    transactionIndex = None
    headers = next(csv_header_reader)
    for i in range(0, len(headers)):
        # print(headers[i])
        if 'Date' in headers[i]:
            dateIndex = i
        elif 'Credit' in headers[i]:
            creditIndex = i
        elif 'Debit' in headers[i]:
            debitIndex = i
        elif 'Transaction' in headers[i]:
            transactionIndex = i
        else:
            debitIndex = i
            creditIndex = i

    with open('formatted-Transaction-1.csv', 'w') as formatted_file:
        csv_writer = csv.writer(formatted_file)
        headers_row = ['Date', 'Transaction Description', 'Debit', 'Credit']
        # print(headers_row)
        row = ['', '', '', '']
        csv_writer.writerow(['', 'Domestic Transactions', '', ''])
        csv_writer.writerow(headers_row)

        def standardize_currency(from_curr, amount):
            c = CurrencyRates()
            # print(amount)
            convertedAmount = c.convert(from_curr, 'INR', amount)
            # convertedAmount = str(convertedAmount)
            # convertedAmount = '0' if convertedAmount[:1] == '0' else convertedAmount
            return '{0:.2f}'.format(convertedAmount)

        for line in csv_file_reader:

            row[0] = line[dateIndex]
            if 'Date' in row[0]:
                continue
            row[1] = line[transactionIndex].strip()
            if len(row[0]) != 0 and creditIndex == debitIndex:
                if 'cr' in line[debitIndex]:
                    row[2] = line[debitIndex].replace(' cr', '')
                    row[3] = '0'
                else:
                    row[2] = '0'
                    row[3] = line[debitIndex]
            else:
                row[2] = line[creditIndex]
                row[3] = line[debitIndex]
            if 'Amount' in row[3]:
                row[2] = 'Credit'
                row[3] = 'Debit'
            else:
                if len(row[0]) != 0 and len(row[2]) == 0:
                    row[2] = 0
                if len(row[0]) != 0 and len(row[3]) == 0:
                    row[3] = 0
            if len(row[0]) == 0 and len(row[3]) == 0:
                strRow = ''.join(row)
                if len(strRow) == 0:
                    continue
                else:
                    csv_writer.writerow(['', strRow, '', ''])
                # print(strRow)
            else:
                tdl = len(row[1])
                tdC = (row[1])[tdl-6:tdl]
                tdC = tdC.strip()
                if len(tdC) == 3:
                    row[1] = (row[1])[:tdl-6].strip()
                    row[2] = standardize_currency(tdC, Decimal(row[2]))
                    # print(row[2])
                    row[3] = standardize_currency(tdC, Decimal(row[3]))
                    # print(row[3])
                    # print(tdC)
                # print(row)
                csv_writer.writerow(row)


