from django.core.exceptions import ValidationError
import re


# checks to see if the input ssn is valid
def validate_ssn(value):
    regex = "^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$"
    p = re.compile(regex)

    # if the string is non or does not match the regex the error is thrown
    if value == None or not (re.search(p, value)):
        raise ValidationError('%(value)s is not a valid ssn', params={'value': value})


def validate_postal_code(value):
    regex = "^(?!.*[DFIOQU])[A-VXY][0-9][A-Z]●?[0-9][A-Z][0-9]$"
    p = re.compile(regex)

    # if the string is non or does not match the regex the error is thrown
    if value == None or not (re.search(p, value)):
        raise ValidationError('%(value)s is not a valid postal code', params={'value': value})
