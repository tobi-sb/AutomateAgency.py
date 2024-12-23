def combine_files(city_file, categories_file, output_file):
    with open(city_file, 'r', encoding='utf-8') as city_f, open(categories_file, 'r', encoding='utf-8') as categories_f:
        cities = city_f.readlines()
        categories = categories_f.readlines()

    with open(output_file, 'w', encoding='utf-8') as output_f:
        for category in categories:
            category = category.strip()
            for city in cities:
                city = city.strip()
                output_f.write(f"{category} {city}\n")

if __name__ == "__main__":
    combine_files('./city.txt', './categories.txt', './combined_output.txt')
