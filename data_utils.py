import xml.etree.ElementTree as ET
from pathlib import Path


def parse_tmx(path):
    tree = ET.parse(path)
    root = tree.getroot()
    result = []
    
    for tu in root.findall(".//tu"):
        content = []

        tuvs = tu.findall("tuv")
        if len(tuvs) != 2:
            print(f"Warning: {len(tuvs)} tuvs")
            
        for tuv in tu.findall("tuv"):
            lang = tuv.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
            seg = tuv.find("seg")
            if seg is not None and seg.text is not None:
                content.append({"lang": lang, "text": seg.text})
        
        if len(content) == 2:
            result.append(content)
        elif len(content) > 2:
            print(f"Skip file: {path}. \nUnexpected content size: {len(content)}")
    
    return result


def create_documents_from_xml(root_dir):
    documents = []
    files = []
    file_id = 0
    directory = Path(root_dir)

    file_paths = [f for f in directory.rglob("*") if f.is_file() and not f.name.startswith(".")]

    for file_path in file_paths:
        try:
            content_list = parse_tmx(file_path)
            for content in content_list:
                try:
                    doc = {
                        "lang": content[0]["lang"],
                        "text": content[0]["text"], 
                        "tr_lang": content[1]["lang"],
                        "tr_text": content[1]["text"],
                        "file_id": file_id
                    }
                    documents.append(doc)
                except Exception as e:
                    print(f"Failed to create doc\nFile: {file_path}\n with content\n: {content}")
                    print(f"Error: {e}\n\n")
                    
            files.append({"id": file_id, "path": str(file_path), "docs_num": len(content_list)})
            file_id += 1

        except ET.ParseError as pe:
            print(f"Failed to process '{file_path}': {pe}\n")

    
    return documents, files
