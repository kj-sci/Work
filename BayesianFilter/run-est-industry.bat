set base_dir=Y:\Data\Koji_Yokoyama
set training_fname=%base_dir%\AIU\DNB\training_tsr_industry.txt
set test_fname=%base_dir%\External\Crawling\company_site_raw\201706\test_1.txt

python bayesian-filter-words.py %training_fname% %test_fname%

