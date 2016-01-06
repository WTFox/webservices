import logins
from webservices import BenefitPoint

bp = BenefitPoint(**logins.benefitpoint)

# Create the complex type
productSearchCriteria = bp.create_type('ns1:ProductSearchCriteria')
productSearchCriteria.accountID = 1344234

# Call the method and send in the complex type, productSearchCriteria, as a param.
productSummaries = bp.call('findProducts', productSearchCriteria)

for product in productSummaries:
    print(product)
