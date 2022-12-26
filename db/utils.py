"""
utils module
"""
from os import environ
from db.record import Record
from supabase import create_client,Client

url: str = "https://dwosibtkxkverqqwtsnp.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR3b3NpYnRreGt2ZXJxcXd0c25wIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzIwMzk2NDAsImV4cCI6MTk4NzYxNTY0MH0.K53kkr3OVpfT0Sw4gq5jSN60hLlZJFj7ZSdcWkUJq9s"
supabase = create_client(url, key)

def add_record(record: Record) -> None:
    try:
        supabase.table("Record").insert(record.RecordToDict()).execute()
    except:
        pass
    return None

def delete_record(record_id: int) -> None:
    try:
        supabase.table("Record").delete().filter("record_id", "eq", record_id).execute()
    except:
        pass
    return None    

def find_record(record_id: int) -> Record:
    try:
        res = supabase.table("Record").select("*").filter("record_id", "eq", record_id).execute().data
        if len(res)==0:
            return None
        return res[0]
    except:
        pass
    return None    

def creditor_records(creditor_id: int) -> list[Record]:
    try:
        return supabase.table("Record").select("*").filter("creditor_id", "eq",creditor_id).execute().data
    except:
        pass
    return None

def debtor_records(debtor_id: int) -> list[Record]:
    try:
        return supabase.table("Record").select("*").filter("debtor_id", "eq", debtor_id).execute().data
    except:
        pass
    return None

