from typing import Any, Dict, List, Optional
import re

import requests
import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession


async def scrape_job_page(url: str, params: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Scrapes a job page for job listings and returns the data as a pandas DataFrame.

    Args:
        url (str): The URL of the job page to scrape.
        params (Optional[Dict[str, str]]): Optional dictionary of query parameters to include in the request.

    Returns:
        pd.DataFrame: A DataFrame containing the job listings.
    """
    if params is None:
        params = {"page": "1"}

    headers = {
        "accept": "application/json",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "priority": "u=1, i",
        "referer": "https://www.catho.com.br/vagas/engenheiro-de-dados/?page=1",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "x-instana-l": "1,correlationType=web;correlationId=46d61ab473660a73",
        "x-instana-s": "46d61ab473660a73",
        "x-instana-t": "46d61ab473660a73",
        "x-nextjs-data": "1",
    }
    response = requests.get(url=url, params=params, headers=headers)
    json_data = response.json()

    jobs: List[Dict[str, Any]] = []

    job_list = json_data["pageProps"]["jobSearch"]["jobSearchResult"]["data"]["jobs"]
    for job_data in job_list:
        job_custom_data = job_data["job_customized_data"]
        job = {
            "title": job_custom_data["titulo"],
            "company": job_custom_data["anunciante"]["nome"],
            "location": job_custom_data["vagas"][0]["cidade"] if job_custom_data["vagas"] else None,
            "vacancies": job_custom_data["jobQuantity"],
            "publication_date": job_custom_data["dataAtualizacao"],
            "salary": job_custom_data["faixaSalarial"],
            "description": job_custom_data.get("descricao", ""),
            "job_id": job_custom_data.get("id", ""),
            "update_date": job_custom_data.get("dataAtualizacao", ""),
            "salary_negotiable": job_custom_data.get("salarioACombinar", False),
            "company_size": job_custom_data.get("companySize", ""),
            "job_type": job_custom_data.get("tipoEmp", ""),
            "additional_info": job_custom_data.get("infoAdicional", ""),
            "contract_type": job_custom_data.get("regimeContrato", ""),
            "benefits": ", ".join(job_custom_data.get("benef", [])),
            "entry_date": job_custom_data.get("entradaEmp", ""),
            "has_questionnaire": job_custom_data.get("possuiQuest", False),
            "job_url": f"https://www.catho.com.br/vagas/{job_custom_data.get('id', '')}"
            if not job_custom_data.get("origemAgregador", "")
            else job_custom_data.get("origemAgregador"),
            "professional_area": job_custom_data.get("perfilId", ""),
        }
        jobs.append(job)

    return pd.DataFrame(jobs)


async def scrape_all_jobs(base_url: str, max_pages: Optional[int] = None, verbose: bool = False) -> pd.DataFrame:
    """
    Scrapes multiple pages of job listings and returns the data as a pandas DataFrame.

    Args:
        base_url (str): The base URL for the job listings.
        max_pages (Optional[int]): The maximum number of pages to scrape. If None, all available pages will be scraped.

    Returns:
        pd.DataFrame: A DataFrame containing all the job listings.
    """
    all_jobs = pd.DataFrame()
    page_number = 1

    while True:
        params = {
            "page": str(page_number),
            "slug": "engenheiro-de-dados",
        }
        if verbose:
            print(f"Going through page {page_number}")
        jobs_df = await scrape_job_page(base_url, params)

        if jobs_df.empty:
            if verbose:
                print(f"No more jobs found at page {page_number}. Stopping.")
            break

        all_jobs = pd.concat([all_jobs, jobs_df], ignore_index=True)

        if max_pages and page_number >= max_pages:
            if verbose:
                print(f"Reached the maximum number of pages: {max_pages}. Stopping.")
            break

        page_number += 1

    return all_jobs


def normalize_string(input_string: str) -> str:
    """
    Converts all characters in the input string to lowercase, replaces spaces with hyphens,
    and strips leading and trailing spaces.

    Args:
        input_string (str): The string to be normalized.

    Returns:
        str: The normalized string.
    """
    return input_string.strip().lower().replace(" ", "-")


async def catho_job_scraper(role: str, base_url: str, max_pages: Optional[int] = None, verbose: bool = False) -> pd.DataFrame:
    """
    Scrapes job listings for a specific role from Catho and returns the data as a pandas DataFrame.

    Args:
        role (str): The job role to search for.
        max_pages (Optional[int]): The maximum number of pages to scrape. If None, all available pages will be scraped.

    Returns:
        pd.DataFrame: A DataFrame containing the job listings for the specified role.
    """
    normalized_role = normalize_string(role)

    url = f"{base_url}{normalized_role}.json"
    return await scrape_all_jobs(base_url=url, max_pages=max_pages, verbose=verbose)


def salario_min_max(texto: str):
    numeros = re.findall(r'\d+\.\d{3},\d{2}', texto)
    if len(numeros) == 2:
        min_valor = float(numeros[0].replace('.', '').replace(',', '.'))
        max_valor = float(numeros[1].replace('.', '').replace(',', '.'))
        return min_valor, max_valor
    if texto.startswith("Até R$ 1.000,00"):
        return np.nan, np.nan
    else:
        return numeros, numeros


def extrair_habilidades(descricao, habilidades=None):
    if habilidades is None:
        habilidades = ["Python", "SQL", "R", "Excel", "Power BI", "Estatística", "Análise de Dados", "Airflow", "AWS", "Hadoop", "Inglês", "Banco de dados", "BigData"]

    if pd.isna(descricao):
        return ""
    encontradas = []
    for habilidade in habilidades:
        if re.search(rf'\b{habilidade}\b', descricao, re.IGNORECASE):
            encontradas.append(habilidade)
    return ", ".join(encontradas)


def format_to_tables(df: pd.DataFrame) -> Dict[str, List[Dict[str, Any]]]:
    df_out = df.copy()

    df_out['Valor Min'] = df['salary'].apply(lambda x: salario_min_max(x)[0])
    df_out['Valor Max'] = df['salary'].apply(lambda x: salario_min_max(x)[1])
    df_out['Habilidades'] = df_out['description'].apply(extrair_habilidades)

    df_out['publication_date'] = pd.to_datetime(df_out['publication_date']).apply(lambda x: x.tz_convert('UTC') if x.tzinfo else x.tz_localize('UTC'))
    df_out['update_date'] = pd.to_datetime(df_out['update_date']).apply(lambda x: x.tz_convert('UTC') if x.tzinfo else x.tz_localize('UTC'))

    formatted_data = {
        "Positions": [],
        "Postings": [],
        "Skills": [],
        "Salaries": [],
        "JobSkills": [],
    }

    skills_map = {}
    job_skills_set = set()

    for index, row in df_out.iterrows():
        position_id = row["job_id"]
        created_at = row["publication_date"]
        updated_at = row["update_date"]
        
        formatted_data["Positions"].append({
            "title": row["title"],
            "description": row["description"],
            "created_at": created_at,
            "updated_at": updated_at,
            "deleted_at": None,
        })
        
        formatted_data["Postings"].append({
            "position_id": position_id,
            "original_title": row["title"],
            "location": row["location"],
            "company": row["company"],
            "seniority": "",
            "created_at": created_at,
            "updated_at": updated_at,
        })
        
        formatted_data["Salaries"].append({
            "posting_id": index,
            "base_salary": row["Valor Min"],
            "median_salary": None,
            "max_salary": row["Valor Max"],
            "currency": "BRL",
            "created_at": created_at,
            "updated_at": updated_at,
        })

        habilidades = row["Habilidades"].split(", ")
        for skill in habilidades:
            if skill not in skills_map:
                skill_id = len(skills_map) + 1
                skills_map[skill] = skill_id
                formatted_data["Skills"].append({
                    "id": skill_id,
                    "name": skill,
                    "created_at": pd.Timestamp.now(tz='UTC'),
                    "updated_at": pd.Timestamp.now(tz='UTC'),
                    "deleted_at": None,
                })
            else:
                skill_id = skills_map[skill]

            job_skill_key = (index, skill_id)
            if job_skill_key not in job_skills_set:
                job_skills_set.add(job_skill_key)
                formatted_data["JobSkills"].append({
                    "posting_id": index,
                    "skill_id": skill_id,
                    "created_at": pd.Timestamp.now(tz='UTC'),
                })
    
    return formatted_data



async def scrape_endpoint(
    role: str,
    base_url: str,
    max_pages: Optional[int],
):
    df = await catho_job_scraper(role, base_url, max_pages)
    formatted_data = format_to_tables(df)

    return formatted_data
