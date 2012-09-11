'''
Created on Sep 9, 2012

@author: staticfish
'''
from kairos.util import get_type
from decimal import Decimal

class GenericAspect(object):

    @staticmethod    
    def validate(rulesets, instance):
        errors = {}
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
                        passed, error = prop_name_method(required_value, operator_type, property_value)                        
                else:
                    #invoke default validator
                    passed, error = GenericValidator.validator(operator_type.code, property_type, required_value, property_value)
                
                if not passed:
                    errors[property_name] = error
        return errors


class GenericValidator(object):
    
    def greater_then_validator(required_value, property_value):
        if property_value > required_value:
            return True, None
        else:
            return False, str(required_value) + ' is not greater than ' + str(property_value)

    def less_then_validator(required_value, property_value):
        if property_value < required_value:
            return True, None
        else:
            return False, str(required_value) + ' is not less than ' + str(property_value)
        
    def equal_to_validator(required_value, property_value):
        if property_value == required_value:
            return True, None
        else:
            return False, str(required_value) + ' is not equal to ' + str(property_value)
    
    operator_mapping = {'GT': greater_then_validator, 'LT': less_then_validator, 'EQ': equal_to_validator}
    
    @staticmethod
    def to_property_type(value_type, value):
        """convert to primitive if its object type"""
        if value_type.code == 'NUM': 
            return int(value)
                    
        return value
    
    @staticmethod
    def validator(operator_type, property_type, required_value, property_value):
        validator_func = GenericValidator.operator_mapping[operator_type]        
        return validator_func(GenericValidator.to_property_type(property_type, required_value), GenericValidator.to_property_type(property_type, property_value))
    
    
