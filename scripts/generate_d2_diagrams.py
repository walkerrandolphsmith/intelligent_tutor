import subprocess
import os

def generate_d2_diagram(input_file, output_file):
    """
    Generate a PNG diagram from a D2 file using the d2 tool.
    
    Args:
        input_file (str): Path to the input D2 file.
        output_file (str): Path to the output PNG file.
    """
    try:
        subprocess.run(["d2", input_file, output_file], check=True)
        print(f"Diagram generated successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating diagram: {e}")

if __name__ == "__main__":
    input_dir = os.path.join(os.path.dirname(__file__), "../diagrams")
    output_dir = os.path.join(os.path.dirname(__file__), "../docs/.attachments")
    os.makedirs(output_dir, exist_ok=True)

    d2_files = [f for f in os.listdir(input_dir) if f.endswith(".d2")]

    for d2_file in d2_files:
        input_file = os.path.join(input_dir, d2_file)
        output_file = os.path.join(output_dir, os.path.splitext(d2_file)[0] + ".png")
        generate_d2_diagram(input_file, output_file)