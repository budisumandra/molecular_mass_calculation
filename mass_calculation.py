from flask import Flask, jsonify, render_template,request
import requests
import re

app = Flask(__name__)

API_BASE_URL = "http://127.0.0.1:5000/search"

def parse_formula(formula):
    pattern = re.compile(r'([A-Z][a-z]?)(\d*)')
    elements = {}

    for match in pattern.findall(formula):
        element = match[0]
        count = int(match[1]) if match[1] else 1
        elements[element] = elements.get(element,0) + count
    
    return elements

def calculate_molecular_mass(elements):
    total_mass = 0
    breakdown = []x 
    
    for element, count in elements.items():
        response = requests.get(f"{API_BASE_URL}?query={element}")
        
        if response.ok:
            data = response.json()
            element_mass = data['atomic_mass']*count
            total_mass += element_mass
            breakdown.append({
                'element' : element,
                'atomic_mass' : data['atomic_mass'],
                'count' : count,
                'element_mass' : element_mass
            })
        else:
            return {'error' : f"ELement '{element}' not found"}
        
    return {'total_mass':total_mass, 'breakdown':breakdown}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_molecular_mass', methods = ['POST'])
def calculate():
    data = request.json
    formula = data.get("formula",'')
    if not formula:
        return jsonify({'error':"Formula is required"}), 400
    elements = parse_formula(formula)
    result = calculate_molecular_mass(elements)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)