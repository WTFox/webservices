# WebServices

This is geared towards insurance agencies, particularly mine, that want to interface with in-house Sagitta and BenefitPoint. 

## Install
* Download the zipfile from the [releases](https://github.com/wtfox/webservices/releases) page and install it. 
* Clone the source: `git clone git://github.com/wtfox/webservices.git` and install it yourself: 
 
   
## Getting Started with Sagitta
* Install requirements
    * ```pip install -r requirements.txt```
* Install WebServices
    * ```python setup.py install```

## Examples
##### logins.py
```python
    benefitpoint = dict(
        username='you@me.com',
        password='benefitpointpass'
    )
    
    sagitta = dict(
        account='example',
        username='jsmith',
        password='SmithRocks!',
        accessCode='',
        serverPool='serverpool1',
        onlineCode='',
        wsServer='server02'
    )
```
##### sagittaExample.py
```python
    import logins
    from webservices import Sagitta
    
    # create the Sagitta object by passing in login creds. see logins.py
    s = Sagitta(**logins.sagitta)
    
    response = s.call('rolodexStartsWith', 'smith')
    print(response)
```
##### benefitpointExample.py
```python
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

```