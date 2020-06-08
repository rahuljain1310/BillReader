""" This file is for storing data useful in
    extracting information from the Bills """

### Bag of Words for different Category ###

currencyBag = ['$', '₹', '¥', '€', '£']
## Exhaustive Lists 

qtyBag = ['QTY', 'Quantity', 'Count']
perUnitCost = ['Item Count', 'Per Item']
priceBag = ['Cost', 'Amount', 'Total']
totalBag = ['Grand Total', 'Final Amount','Invoice Total', 'Total']
TermBag = ['Discount', 'Tax', 'Sub Total', 'Subtotal']
HeaderBag = ['Sno', '#', 'Description', 'Unit Cost', 'QTY/HR Rate', 'Item & Description']

Keywords = qtyBag + perUnitCost + priceBag + totalBag + TermBag + HeaderBag
Keywords = [s.lower() for s in Keywords]