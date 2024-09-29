#!/usr/bin/python3

import jinja2
from itertools import product

# Jinja2 template 1 (original kevko template)
template_orig_kevko = """
{{
  'internal' if enable_letsencrypt  and kolla_same_external_internal_vip  and letsencrypt_internal_cert_server != ''
  else (
    'internal,external' if enable_letsencrypt  and letsencrypt_internal_cert_server != '' and letsencrypt_external_cert_server != ''
    else (
      'internal' if enable_letsencrypt  and letsencrypt_internal_cert_server != ''
      else (
        'external' if enable_letsencrypt  and not kolla_same_external_internal_vip  and letsencrypt_external_cert_server != ''
        else ''
      )
    )
  )
}}
"""

# Jinja2 template 2 (suggested sven template)
template_suggested_sven = """
{{
  'internal' if enable_letsencrypt and kolla_same_external_internal_vip and letsencrypt_internal_cert_server != '' and letsencrypt_external_cert_server == ''
  else (
    'internal,external' if enable_letsencrypt and letsencrypt_internal_cert_server != '' and letsencrypt_external_cert_server != ''
    else (
      'internal' if enable_letsencrypt and letsencrypt_internal_cert_server != ''
      else (
        'external' if enable_letsencrypt and not kolla_same_external_internal_vip and letsencrypt_external_cert_server != ''
        else ''
      )
    )
  )
}}
"""

# Jinja2 template 3 (simplified kevko template)
template_simplified_kevko = """
{{
  '' if not enable_letsencrypt
  else (
    'internal' if letsencrypt_internal_cert_server != '' and kolla_same_external_internal_vip
    else (
      'internal,external' if letsencrypt_internal_cert_server != '' and letsencrypt_external_cert_server != ''
      else (
        'internal' if letsencrypt_internal_cert_server != ''
        else (
          'external' if letsencrypt_external_cert_server != '' and not kolla_same_external_internal_vip
          else ''
        )
      )
    )
  )
}}
"""

# Create Jinja2 environment
env = jinja2.Environment()

# Compile the templates
template_1 = env.from_string(template_orig_kevko)
template_2 = env.from_string(template_suggested_sven)
template_3 = env.from_string(template_simplified_kevko)

# Generate all combinations of True/False for the boolean values and ''/'server' for the certificate strings
boolean_combinations = list(product([True, False], repeat=2))  # for enable_letsencrypt, kolla_same_external_internal_vip
cert_combinations = list(product(['', 'server'], repeat=2))    # for letsencrypt_internal_cert_server and letsencrypt_external_cert_server

# All test cases
test_cases = [
    {
        'enable_letsencrypt': enable_letsencrypt,
        'kolla_same_external_internal_vip': kolla_same_external_internal_vip,
        'letsencrypt_internal_cert_server': letsencrypt_internal_cert_server,
        'letsencrypt_external_cert_server': letsencrypt_external_cert_server,
    }
    for (enable_letsencrypt, kolla_same_external_internal_vip) in boolean_combinations
    for (letsencrypt_internal_cert_server, letsencrypt_external_cert_server) in cert_combinations
]

# Function to get expected results based on the logic
def get_expected_result(enable_letsencrypt, kolla_same_external_internal_vip, letsencrypt_internal_cert_server, letsencrypt_external_cert_server):
    if not enable_letsencrypt:
        return ""
    if letsencrypt_internal_cert_server != '' and kolla_same_external_internal_vip:
        return 'internal'
    if letsencrypt_internal_cert_server != '' and letsencrypt_external_cert_server != '':
        return 'internal,external'
    if letsencrypt_internal_cert_server != '':
        return 'internal'
    if letsencrypt_external_cert_server != '' and not kolla_same_external_internal_vip:
        return 'external'
    return ""

# Function to run tests on a given template
def run_tests(template, template_name):
    print(f"\n--- Running tests for {template_name} ---")
    for i, test_case in enumerate(test_cases):
        # Render the template with the current values
        output = template.render(**test_case).strip().replace('\n', '')
        expected = get_expected_result(**test_case)
        
        # Print input parameters, expected and actual output
        print(f"\nTest case {i+1}:")
        print(f"  Input parameters: {test_case}")
        print(f"  Expected: \"{expected}\"")
        print(f"  Got: \"{output}\"")
        
        # Check if the output matches the expected result
        if output == expected:
            print(f"  Result: Passed!")
        else:
            print(f"  Result: Failed!")

# Run tests for all three templates
run_tests(template_1, "Template Original Kevko")
run_tests(template_2, "Template Suggested Sven")
run_tests(template_3, "Template Simplified Kevko")
