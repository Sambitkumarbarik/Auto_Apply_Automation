import argparse

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Naukri Auto Apply Bot')
    
    parser.add_argument('--role', 
                      type=str, 
                      required=True,
                      help='Job role to search for')
    
    parser.add_argument('--location', 
                      type=str, 
                      required=True,
                      help='Job location to filter by')
    
    parser.add_argument('--experience', 
                      type=int, 
                      required=True,
                      help='Years of experience')
    
    parser.add_argument('--freshness', 
                      type=int, 
                      choices=[1, 3, 7, 15, 30],
                      required=True,
                      help='Job freshness in days (1, 3, 7, 15, or 30)')
    
    parser.add_argument('--limit', 
                      type=int, 
                      default=20,
                      help='Maximum number of jobs to apply (default: 20)')

    return parser.parse_args()
