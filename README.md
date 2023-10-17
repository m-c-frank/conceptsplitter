# conceptsplitter

conceptsplitter is a project designed to extract atomic concepts from a given text. It utilizes the OpenAI API to analyze and split the text into distinct core concepts, ensuring that each concept is clearly defined and elaborated upon. The project is particularly useful for extracting and organizing information from large text dumps, such as those from websites.

## Features

- Extract atomic concepts from a given text.
- Utilizes OpenAI API for sophisticated parsing.
- Saves extracted concepts as individual text files.
- Provides a clear structure for analyzing and splitting text based on specific guidelines.

## Directory Structure

```bash
.
├── .gitignore           # Git ignore file
├── _.env                # Environment variables (contains OpenAI API key)
├── concept_split.ppt    # Guidelines and example for text analysis
├── interface.py         # Interface to OpenAI API and core functions
├── requirements.txt     # Project dependencies
└── split_concepts.py    # Main script to process and save extracted concepts
```

## Setup

1. Clone the repository:

    ```bash
    git clone [repository_url]
    cd conceptsplitter
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your OpenAI API key:
   - Obtain your OpenAI API key from the OpenAI platform.
   - Open the `_.env` file and replace `your_api_key_here` with your actual API key.
   - rename the file to `.env` (remove the underscore).

## Usage

1. Place the text files you want to process in the `~/Downloads` directory. Ensure that the filenames start with the prefix `text-`.

2. Run the main script:

   ```bash
   python split_concepts.py
   ```

3. Extracted concepts will be saved as individual text files in the `~/desktop/atomic_notes` directory.

## Related Tools
<!--START_TOKEN-->
**Note Utilities Ecosystem**: A suite of tools designed to streamline and enhance your note-taking and information processing workflows.

- **[workflowlibrary](https://github.com/m-c-frank/workflowlibrary)** - Centralizes and synchronizes the "Related Tools" section across the ecosystem.
- **[noteutilsyncer](https://github.com/m-c-frank/noteutilsyncer)** - A centralized tool that automates the synchronization of the "Related Tools" section across READMEs in the noteutils ecosystem.
- **[conceptsplitter](https://github.com/m-c-frank/conceptsplitter)** - Extract atomic concepts from a given text using the OpenAI API.
- **[textdownloader](https://github.com/m-c-frank/textdownloader)** - A browser extension to automatically generate text dumps for processing.
- **[contenttree](https://github.com/m-c-frank/contenttree)** - A utility to print a repository's tree structure and file content
<!--END_TOKEN-->

## Contributing

Contributions to the conceptsplitter project or the note utilities ecosystem are welcome. If you have ideas for improvements or new features, please feel free to submit issues, suggestions, or pull requests in this repository or contact me!

## License

The textdownloader browser extension is open-source and licensed under the [GOS License](https://github.com/m-c-frank/textdownloader/blob/main/LICENCE.md).

## Credits

The conceptsplitter project is developed and maintained by [Martin Christoph Frank](https://github.com/m-c-frank). If you have any questions or need assistance, please contact [martin7.frank7@gmail.com](martin7.frank7@gmail.com).
