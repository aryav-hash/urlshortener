import string
# URL Shortener
# Let's try to generate a shortened url from a big url like that of an amazon product.
url = "https://www.amazon.in/Adjustable-Strengthener-Mechanical-Resistance-Workouts/dp/B0FDB3JPVM/?_encoding=UTF8&ref_=pd_hp_d_atf_dealz_cs"

def generate_url(index):
    characters = string.digits + string.ascii_lowercase + string.ascii_uppercase

    if index == 0:
        return characters[0]

    result = []
    while index > 0:
        rem = index % 62
        result.append(characters[rem])
        index = index // 62
    
    return ''.join(reversed(result))

print(f"The result is: {generate_url(12432)}")
