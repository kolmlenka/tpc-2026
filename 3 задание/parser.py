import os
from typing import List, Tuple

def load_nerel_data(folder_path: str) -> Tuple[List[str], List[List[Tuple[int, int, str]]]]:
    texts = []
    all_entities = []
    
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            txt_path = os.path.join(folder_path, file)
            ann_path = os.path.join(folder_path, file.replace('.txt', '.ann'))
            
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            entities = []

            if os.path.exists(ann_path):
                with open(ann_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if line.startswith('T'):
                            parts = line.strip().split('\t')
                            if len(parts) >= 2:
                                details = parts[1].split(' ')
                                if len(details) >= 3:
                                    entity_type = details[0]
                                    start_str = details[1]
                                    end_str = details[2]
                                    
                                    #скип разрывных сущностей
                                    if ';' in start_str or ';' in end_str:
                                        continue
                                    
                                    start = int(start_str)
                                    end = int(end_str)
                                    entities.append((start, end, entity_type))
            
            texts.append(text)
            all_entities.append(entities)
    
    print("загружено " + str(len(texts)) + " текстов")
    return texts, all_entities
