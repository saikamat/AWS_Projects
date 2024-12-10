import os
import urllib.parse

def generate_markdown_from_images(images_dir, output_file):
    """
    Generates a markdown file with all PNG images from the specified directory,
    handling filenames with spaces or special characters.

    Args:
        images_dir (str): Path to the directory containing PNG images.
        output_file (str): Path to the output markdown file.
    """
    try:
        # Get all PNG files in the directory
        png_files = [f for f in os.listdir(images_dir) if f.endswith('.png')]

        # Sort the files alphabetically
        png_files.sort()

        # Open the output markdown file
        with open(output_file, 'w') as md_file:
            for image in png_files:
                # Encode the filename to handle spaces and special characters
                encoded_image = urllib.parse.quote(image)
                # Write the markdown syntax for each image
                md_file.write(f"![image](./{images_dir}/{encoded_image})\n\n")

        print(f"Markdown file '{output_file}' has been created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Define the directory containing images and the output markdown file
images_directory = "03-Deploying_SQL_Server_databases_on_Amazon_RDS/assets"
output_markdown_file = "output.md"

# Generate the markdown file
generate_markdown_from_images(images_directory, output_markdown_file)