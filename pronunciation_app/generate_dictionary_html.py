import csv

def generate_html_from_csv(csv_file="dic.csv", html_file="search.html"):
    # Load dictionary from CSV
    dictionary = {}
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = str(row.get("name", "")).strip()
                meaning = str(row.get("meaning", "")).strip()
                if word:
                    dictionary[word] = meaning
    except UnicodeDecodeError:
        with open(csv_file, "r", encoding="latin-1") as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = str(row.get("name", "")).strip()
                meaning = str(row.get("meaning", "")).strip()
                if word:
                    dictionary[word] = meaning

    # Generate HTML content
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Student Dictionary</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5; }
        h1 { text-align: center; color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); background-color: #fff; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even){ background-color: #f2f2f2; }
        tr:hover { background-color: #d1e7dd; }
        input[type="text"] { width: 50%; padding: 8px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px; }
    </style>
    <script>
        function searchWord() {
            var input = document.getElementById("searchInput").value.toLowerCase();
            var table = document.getElementById("dictionaryTable");
            var tr = table.getElementsByTagName("tr");
            for (var i = 1; i < tr.length; i++) {
                var tdWord = tr[i].getElementsByTagName("td")[0];
                if (tdWord) {
                    var wordText = tdWord.textContent || tdWord.innerText;
                    tr[i].style.display = wordText.toLowerCase().indexOf(input) > -1 ? "" : "none";
                }
            }
        }
    </script>
</head>
<body>
    <h1>Student Dictionary</h1>
    <center><input type="text" id="searchInput" onkeyup="searchWord()" placeholder="Search for a word..."></center>
    <table id="dictionaryTable">
        <tr><th>Word</th><th>Meaning</th></tr>
"""

    # Add dictionary words as table rows
    for word, meaning in sorted(dictionary.items()):
        html_content += f'        <tr><td>{word}</td><td>{meaning}</td></tr>\n'

    # Close HTML
    html_content += """
    </table>
</body>
</html>
"""

    # Write to HTML file
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML dictionary generated: {html_file}")

# ---------------- Main ----------------
if __name__ == "__main__":
    generate_html_from_csv("dic.csv", "search.html")