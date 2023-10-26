import argparse
import logging
from .split_concept import main as split_concept_main

def main():
    """Main function to handle command-line arguments and setup logging."""
    parser = argparse.ArgumentParser(description="Concept Extraction from Markdown")
    parser.add_argument(
        "input_directory", help="Path to the directory containing markdown files"
    )
    parser.add_argument(
        "--output",
        default="./output",
        help="Path to the output directory where the notes will be saved",
    )
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help="Increase verbosity of logging: -v for WARN, -vv for INFO, -vvv for DEBUG."
    )

    args = parser.parse_args()

    # Adjust the logging level based on verbosity argument
    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels)-1, args.verbose)]
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Call the main function from split_concept with parsed arguments
    split_concept_main(args.input_directory, args.output)

if __name__ == "__main__":
    main()
