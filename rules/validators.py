'''
Created on Sep 9, 2012

@author: staticfish
'''
from kairos.util import get_type

class GenericValidator(object):
    '''
        Generic validator that child classes can overide
    '''
    
    def __init__(self, *args, **kwargs):
        self.operator_mapping = {'GT': self.greater_then_validator, 
                                 'LT': self.less_then_validator, 
                                 'EQ': self.equal_to_validator, 
                                 'GE': self.greater_than_equal_to_validator}
    
    def greater_then_validator(self, required_value, property_value):
        if property_value > required_value:
            return True, None, required_value, property_value
        else:
            return False, str(required_value) + ' is not greater than ' + str(property_value), required_value, property_value
    
    def equal_to_validator(self, required_value, property_value):
        if property_value == required_value:
            return True, None, required_value, property_value
        else:
            return False, str(required_value) + ' is not equal to ' + str(property_value), required_value, property_value
    
    def greater_than_equal_to_validator(self, required_value, property_value):
        validated_data = self.greater_then_validator(required_value, property_value)
        if not validated_data[0]:
            validated_data = self.equal_to_validator(required_value, property_value)
        
        return validated_data
        
    def less_then_validator(self, required_value, property_value):
        if property_value < required_value:
            return True, None, required_value, property_value
        else:
            return False, str(required_value) + ' is not less than ' + str(property_value), required_value, property_value
    
    def to_property_type(self, value_type, value):
        """convert to primitive if its object type"""
        if value_type.code == 'NUM': 
            return int(value)
                    
        return value
    
    def validate(self, operator_type, property_type, required_value, property_value):
        '''
        Validater calls the appropriate function that maps to the operator mapping
        '''
        validator_func = self.operator_mapping[operator_type]        
        return validator_func(self.to_property_type(property_type, required_value), self.to_property_type(property_type, property_value))
    
generic_validator = GenericValidator()    

class ValidatorObject(object):
    '''
        This object will contain all of the properties that got validated, with property name as attribute and value as 
        a tuple of (passed, error_message, expected, actual)
    '''
    pass

class GenericAspect(object):

    @staticmethod    
    def validate(rulesets, instance, validator=None):
        if not validator:
            validator = generic_validator
            
        validated_instance = ValidatorObject()
        has_errors = False
        
        for ruleset in rulesets:
            validator_module = ruleset.validator_module
            if validator_module:
                    validator_module = get_type(validator_module)()
                    
            pointcuts = ruleset.pointcuts.all()
            for pointcut in pointcuts:
                required_value = pointcut.rule.required_value
                operator_type = pointcut.rule.operator_type
                property_name = pointcut.jointpoint.property_name
                property_type = pointcut.jointpoint.property_type
                property_value = getattr(instance, property_name, None)
            
                if not property_value:
                    continue
                #if validator instance is available, lets go with it
                if validator_module:
                    #check whether it has method with `<property_name>_validate
                    #if not resort to default `validate` method, which is expected in `validator_module`
                    prop_name = property_name + '_validate'
                    prop_name_method = getattr(validator_module, prop_name, None)
                    if prop_name_method and callable(prop_name_method):
                        validated_outcome = prop_name_method(required_value, operator_type, property_value)                        
                else:
                    #invoke default validator
                    validated_outcome = validator.validate(operator_type.code, property_type, required_value, property_value)
                
                #check if error occured, so we can let callers know there are errors in the instance
                if not has_errors and not validated_outcome[0]:
                    has_errors = True
                    
                #add this to 
                setattr(validated_instance, property_name, validated_outcome)                
        
        setattr(validated_instance, 'has_errors', has_errors)
        
        return validated_instance