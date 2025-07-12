import csv

# input_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\2024_fb_ads_president_scored_anon.csv"
# output_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\2024_fb_ads_president_scored_anon_cleaned.csv"

# input_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\2024_fb_posts_president_scored_anon.csv"
# output_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\2024_fb_posts_president_scored_anon_cleaned.csv"

input_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\2024_tw_posts_president_scored_anon.csv"
output_path = r"C:\Users\Hrush\Desktop\Semesters\OPT Research\Datasets\2024_tw_posts_president_scored_anon_cleaned.csv"



def clean_csv(input_path, output_path):
    with open(input_path, newline='', encoding='utf-8') as infile, \
         open(output_path, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = [col.strip().lower().replace(" ", "_") for col in reader.fieldnames]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            cleaned_row = {}
            for key, value in zip(fieldnames, row.values()):
                val = value.strip()

                # Standardize nulls
                if val.lower() in ("", "null", "na"):
                    val = ""

                cleaned_row[key] = val

            if any(cleaned_row.values()):  # skip completely empty rows
                writer.writerow(cleaned_row)

    print(f" Cleaned CSV written to: {output_path}")

# Run it
clean_csv(input_path, output_path)
