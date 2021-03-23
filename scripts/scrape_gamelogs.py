import datetime
import urllib.request
import sys
import os
import tarfile

# Get download links
def get_url_list(start_date, end_date):
    timespan = (end_date - start_date + datetime.timedelta(days=1)).days
    date_list = [start_date +
                 datetime.timedelta(days=x) for x in range(timespan)]
    date_list = [str(date).replace('-', '') for date in date_list]
    url_list = ['https://dominion.isotropic.org/gamelog/' +
                date[:4] + '/' + date + '.tar.bz2' for date in date_list]
    return url_list

# Extract downloaded directories
def extract_files(directories):
    for dir in directories:
        try:
            tar = tarfile.open(dir, "r:bz2")
            tar.extractall(destination)
            tar.close()
            os.remove(dir)
        except:
            continue


if __name__ == '__main__':

    start_date = datetime.date(2010, 10, 11)
    end_date = datetime.date(2013, 3, 15)

    # Usage instructions
    if not (len(sys.argv) >= 2):
        sys.stdout.write("\nImproper number of arguments given.\n\n")
        sys.stdout.write("Usage: scrape_gamelogs.py <destination directory> <flags>\nFlags:\n\t-h\tHelp\n\t-u\tUnpack all downloaded files. Warning: uncompressed data size exceeds 100GB.\n\t-d <start date>\tStart date in YYYY-MM-DD format.\n\t-D <end date>\tEnd date in YYYY-MM-DD format.\n\n")
        sys.exit(1)

    if '-h' in sys.argv:
        sys.stdout.write("Usage: scrape_gamelogs.py <destination directory> <flags>\nFlags:\n\t-h\tHelp\n\t-u\tUnpack all downloaded files. Warning: uncompressed data size exceeds 100GB.\n\t-d <start date>\tStart date in YYYY-MM-DD format.\n\t-D <end date>\tEnd date in YYYY-MM-DD format.\n\n")
        sys.exit(0)
        
    if '-d' in sys.argv:
        #try:
        date_string = sys.argv[sys.argv.index('-d')+1]
        y, m, d = date_string.split('-')
        start_date = datetime.date(int(y),int(m),int(d))
        '''except:
            sys.stdout.write("\nError parsing start date. Ensure that the format is YYYY-MM-DD.\n\n")
            sys.exit(2)'''
    
    if '-D' in sys.argv:
        try:
            date_string = sys.argv[sys.argv.index('-D')+1]
            y, m, d = date_string.split('-')
            end_date = datetime.date(int(y),int(m),int(d))
        except:
            sys.stdout.write("\nError parsing end date. Ensure that the format is YYYY-MM-DD.\n\n")
            sys.exit(2)

    if end_date < start_date:
        temp_date = end_date
        end_date = start_date
        start_date = temp_date
    if start_date < datetime.date(2010, 10, 11):
        start_date = datetime.date(2010, 10, 11)
        sys.stdout.write("\nData is only available from 2010-10-11 to 2013-03-16.\n\n")
    if end_date > datetime.date(2013, 3, 15):
        end_date = datetime.date(2013, 3, 15)
        sys.stdout.write("\nData is only available from 2010-10-11 to 2013-03-16.\n\n")

    # Check destination directory
    destination = sys.argv[1] + '/'
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)
    except OSError:
        sys.stdout.write("Invalid directory\n")
        sys.exit(3)

    # Download game data
    urls = get_url_list(start_date, end_date)
    err_count = 0
    for url in urls:
        try:
            filename = destination + \
                url.replace('https://dominion.isotropic.org/gamelog/', '')[5:]
            urllib.request.urlretrieve(url, filename=filename)
        except:
            err_count += 1
            continue

    # Unpack game data
    if len(sys.argv) > 2:
        if '-u' in sys.argv[2:]:
            directories = [destination + url.replace('https://dominion.isotropic.org/gamelog/', '')[5:] for url in urls]
            extract_files(directories)

    if err_count > 0:
        sys.stdout.write(
            "Error during retrieval of one or more files. Some files may be missing.\n")
