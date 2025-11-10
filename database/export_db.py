import mysql.connector
import os
from datetime import datetime


DB_CONFIG = {
    'host': 'localhost',
    'user': 'lsf_user',  
    'password': 'localservicefinder@20',  
    'database': 'lsf_db'
}

OUTPUT_FOLDER = 'database'

def export_database():
    """Export database schema and data to SQL file"""
    
    # Create output folder if not exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(OUTPUT_FOLDER, f'lsf_backup_{timestamp}.sql')
    
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"-- Local Service Finder Database Backup\n")
            f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Database: {DB_CONFIG['database']}\n\n")
            
            f.write(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`;\n")
            f.write(f"USE `{DB_CONFIG['database']}`;\n\n")
            
            # Get all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            for (table_name,) in tables:
                print(f"Exporting table: {table_name}")
                
                # Get CREATE TABLE statement
                cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                create_table = cursor.fetchone()[1]
                
                f.write(f"\n-- Table structure for `{table_name}`\n")
                f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                f.write(f"{create_table};\n\n")
                
                # Get table data
                cursor.execute(f"SELECT * FROM `{table_name}`")
                rows = cursor.fetchall()
                
                if rows:
                    # Get column names
                    cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
                    columns = [col[0] for col in cursor.fetchall()]
                    
                    f.write(f"-- Dumping data for table `{table_name}`\n")
                    f.write(f"INSERT INTO `{table_name}` (`{'`, `'.join(columns)}`) VALUES\n")
                    
                    for i, row in enumerate(rows):
                        # Convert row values to SQL format
                        values = []
                        for val in row:
                            if val is None:
                                values.append('NULL')
                            elif isinstance(val, str):
                                # Escape single quotes
                                escaped = val.replace("'", "''")
                                values.append(f"'{escaped}'")
                            elif isinstance(val, (int, float)):
                                values.append(str(val))
                            elif isinstance(val, datetime):
                                values.append(f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'")
                            else:
                                values.append(f"'{str(val)}'")
                        
                        # Write row
                        if i == len(rows) - 1:
                            f.write(f"({', '.join(values)});\n\n")
                        else:
                            f.write(f"({', '.join(values)}),\n")
        
        cursor.close()
        conn.close()
        
        print(f"\n✓ Database exported successfully to: {output_file}")
        return output_file
        
    except mysql.connector.Error as err:
        print(f"✗ Error exporting database: {err}")
        return None

if __name__ == "__main__":
    print("Starting database export...\n")
    export_database()