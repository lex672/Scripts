import shodan
import openai
import argparse

def get_shodan_query(api_key_openai, user_prompt):
    openai.api_key = api_key_openai
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Convierte la siguiente consulta en lenguaje natural a un query de búsqueda en Shodan."},
                {"role": "user", "content": user_prompt}
            ]
        )
        #return response["choices"][0]["message"]["content"].strip()
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error al procesar la consulta con OpenAI: {e}")
        return None

def search_shodan(api_key_shodan, query):
    try:
        api = shodan.Shodan(api_key_shodan)
        results = api.search(query)
        
        print(f"Resultados encontrados: {results['total']}")
        for result in results['matches']:
            print("IP:", result['ip_str'])
            print("Organización:", result.get('org', 'N/A'))
            print("País:", result.get('location', {}).get('country_name', 'N/A'))
            print("Puerto:", result['port'])
            print("------")
    except shodan.APIError as e:
        print(f"Error en la consulta: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consulta la API de Shodan usando lenguaje natural con OpenAI.")
    parser.add_argument("--api_key_openai", help="Clave API de OpenAI", required=True)
    parser.add_argument("--api_key_shodan", help="Clave API de Shodan", required=True)
    parser.add_argument("--prompt", help="Consulta en lenguaje natural para Shodan", required=True)
    args = parser.parse_args()
    