from data_helpers import query_result, data_preprocess
import streamlit as st


@st.cache(ttl=60*60*6, suppress_st_warning=True)
def get_all_data():
    """
    Combines all the supply and demand metrics.
    """
    
    print('Running queries to get all data')
    
    supply_data = get_supply_data()
    matching_data = get_matching_data()
    selfserv_data = get_selfserv_data()
    
    glossary = get_glossary()
    
    return supply_data, matching_data, selfserv_data, glossary


def get_glossary():
    """
    Function to help make glossary.
    """
    
    glossary = {
        'total_signups_row': 'No. of developers who signed up on Turing platform from RoW region'
      , 'total_signups_latam': 'No. of developers who signed up on Turing platform from LATAM region'
      , 'resume_uploaded_row': 'No. of developers who uploaded their resume on Turing platform from RoW region'
      , 'resume_uploaded_latam': 'No. of developers who uploaded their resume on Turing platform from LATAM region'
      , 'signup_completed_row': 'No. of developers who filled their basic info page on Turing platform from RoW region'
      , 'signup_completed_latam': 'No. of developers who filled their basic info page on Turing platform from LATAM region'
      , 'seniority_assessment_taken_row': 'No. of developers who started taking seniority assessment test from RoW region'
      , 'seniority_assessment_taken_latam': 'No. of developers who started taking seniority assessment test from LATAM region'
      , 'seniority_assessment_drop_off_row': 'No. of developers who dropped off after starting seniority assessment test from RoW region'
      , 'seniority_assessment_drop_off_latam': 'No. of developers who dropped off after starting seniority assessment test from LATAM region'
      , 'devs_taking_mcqs_row': 'No. of developers who started taking technical MCQs from RoW region'
      , 'devs_taking_mcqs_latam': 'No. of developers who started taking technical MCQs from LATAM region'
      , 'devs_taking_demand_forecasted_row': 'No. of developers taking mcqs which are expected to be in demand from RoW region'
      , 'devs_taking_demand_forecasted_latam': 'No. of developers taking mcqs which are expected to be in demand from LATAM region'
      , 'mcq_dropoff_row': 'No. of developers who are dropping in between mcqs from RoW region'
      , 'mcq_dropoff_latam': 'No. of developers who are dropping in between mcqs from LATAM region'
      , 'devs_passing_mcqs_row': 'No. of developers who are passing in mcqs from RoW region'
      , 'devs_passing_mcqs_latam': 'No. of developers who are passing in mcqs from LATAM region'
      , 'devs_passing_demand_forecasted_mcqs_row': 'No. of developers passing mcqs which are expected to be in demand from RoW region'
      , 'devs_passing_demand_forecasted_mcqs_latam': 'No. of developers passing mcqs which are expected to be in demand from LATAM region'
      , 'devs_taking_acc_row': 'No. of developers who are taking ACC from the RoW region'
      , 'devs_taking_acc_latam': 'No. of developers who are taking ACC from the LATAM region'
      , 'acc_dropoff_row': 'No. of developers who are dropping off in between ACC from the RoW region'
      , 'acc_dropoff_latam': 'No. of developers who are dropping off in between ACC from the LATAM region'
      , 'devs_passing_acc_row': 'No. of developers who are passing ACC from the RoW region'
      , 'devs_passing_acc_latam': 'No. of developers who are passing ACC from the LATAM region'
      , 'devs_vetted_row': 'No. of vetted developers from the RoW region'
      , 'devs_vetted_latam': 'No. of vetted developers from the LATAM region'
      , 'p2_portal_logins_row': 'No. of developers who login on the P2 Portal from the RoW region'
      , 'p2_portal_logins_latam': 'No. of developers who login on the P2 Portal from the LATAM region'
      , 'resume_updates_row': 'No. of resume updates by developers from the RoW region'
      , 'resume_updates_latam': 'No. of resume updates by developers from the LATAM region'
      , 'p2_taking_mcq_row': 'No. of P2 developers taking mcqs from the RoW region'
      , 'p2_taking_mcq_latam': 'No. of P2 developers taking mcqs from the LATAM region'
      , 'p2_passing_mcq_row': 'No. of P2 developers passing mcqs from the RoW region'
      , 'p2_passing_mcq_latam': 'No. of P2 developers passing mcqs from the LATAM region'
      , 'self_serve_pool_row': 'No. of developers in the self serve pool from the RoW region'
      , 'self_serve_pool_latam': 'No. of developers in the self serve pool from the LATAM region'
      , 'ss_interview_requests_fss_existing': 'No. of interview requests from the SS Pool by FSS Existing category'
      , 'ss_interview_requests_fss_new': 'No. of interview requests from the SS Pool by FSS New category'
      , 'ss_interview_requests_platinum_existing': 'No. of interview requests from the SS Pool by Enterprise Existing category'
      , 'ss_interview_requests_platinum_new': 'No. of interview requests from the SS Pool by Enterprise New category'
      , 'ss_interviews_happened_fss_existing': 'No. of interview happened from the SS Pool by FSS Existing category'
      , 'ss_interviews_happened_fss_new': 'No. of interview happened from the SS Pool by FSS New category'
      , 'ss_interviews_happened_platinum_existing': 'No. of interview happened from the SS Pool by Enterprise Existing category'
      , 'ss_interviews_happened_platinum_new': 'No. of interview happened from the SS Pool by Enterprise New category'
      , 'ss_devs_chosen_fss_existing': 'No. of devs chosen from the SS Pool by FSS Existing category'
      , 'ss_devs_chosen_fss_new': 'No. of devs chosen from the SS Pool by FSS New category'
      , 'ss_devs_chosen_platinum_existing': 'No. of devs chosen from the SS Pool by Enterprise Existing category'
      , 'ss_devs_chosen_platinum_new': 'No. of devs chosen from the SS Pool by Enterprise New category'
      , 'ss_searches_fss': 'No. of SS Query searches by FSS category'
      , 'ss_searches_platinum': 'No. of SS Query searches by Enterprise category'
      , 'ss_profile_viewed_fss': 'No. of SS Profile Viewed by FSS category'
      , 'ss_profile_viewed_platinum': 'No. of SS Profile Viewed by Enterprise category'
      , 'ss_signin_failure_fss': 'Percentage of SS Sign-in Failures by FSS category'
      , 'ss_signin_failure_platinum': 'Percentage of SS Sign-in Failures by Enterprise category'
      , 'ss_client_latency_perc50': 'SS Client Latency Percentile 50'
      , 'devs_shortlisted_fss_existing': 'No. of devs shortlisted from Matching by FSS Existing Category'
      , 'devs_shortlisted_fss_new': 'No. of devs shortlisted from Matching by FSS New Category'
      , 'devs_shortlisted_platinum_existing': 'No. of devs shortlisted from Matching by Enterprise Existing Category'
      , 'devs_shortlisted_platinum_new': 'No. of devs shortlisted from Matching by Enterprise New Category'
      , 'packets_sent_fss_existing': 'No. of packets sent from Matching by FSS Existing Category'
      , 'packets_sent_fss_new': 'No. of packets sent from Matching by FSS New Category'
      , 'packets_sent_platinum_existing': 'No. of packets sent from Matching by Enterprise Existing Category'
      , 'packets_sent_platinum_new': 'No. of packets sent from Matching by Enterprise New Category'
      , 'ms_interview_requests_fss_existing': 'No. of interview request from Matching by FSS Existing Category'
      , 'ms_interview_requests_fss_new': 'No. of interview request from Matching by FSS New Category'
      , 'ms_interview_requests_platinum_existing': 'No. of interview request from Matching by Enterprise Existing Category'
      , 'ms_interview_requests_platinum_new': 'No. of interview request from Matching by Enterprise New Category'  
      , 'ms_interviews_happened_fss_existing': 'No. of interview happened from Matching by FSS Existing Category'
      , 'ms_interviews_happened_fss_new': 'No. of interview happened from Matching by FSS New Category'
      , 'ms_interviews_happened_platinum_existing': 'No. of interview happened from Matching by Enterprise Existing Category'
      , 'ms_interviews_happened_platinum_new': 'No. of interview happened from Matching by Enterprise New Category'
      , 'ms_devs_chosen_fss_existing': 'No. of devs chosen from Matching by FSS Existing Category'
      , 'ms_devs_chosen_fss_new': 'No. of devs chosen from Matching by FSS New Category'
      , 'ms_devs_chosen_platinum_existing': 'No. of devs chosen from Matching by Enterprise Existing Category'
      , 'ms_devs_chosen_platinum_new': 'No. of devs chosen from Matching by Enterprise New Category'
      , 'ms_client_latency_perc50': 'MS Client Latency Percentile 50'
    }
    
    return glossary


def get_selfserv_data():
    """
    Function to get selfserv data.
    
    Returns:
        (dict): Containing all the metric names and their data pairs. 
    """

    self_serve_pool_row, self_serve_pool_latam = get_self_serve_pool()
    ss_interview_requests_fss_existing, ss_interview_requests_fss_new, ss_interview_requests_platinum_existing, ss_interview_requests_platinum_new = get_ss_interview_requests()
    ss_interviews_happened_fss_existing, ss_interviews_happened_fss_new, ss_interviews_happened_platinum_existing, ss_interviews_happened_platinum_new = get_ss_interviews_happened()
    ss_devs_chosen_fss_existing, ss_devs_chosen_fss_new, ss_devs_chosen_platinum_existing, ss_devs_chosen_platinum_new = get_ss_devs_chosen()
    ss_searches_fss, ss_searches_platinum = get_ss_searches()
    ss_profile_viewed_fss, ss_profile_viewed_platinum = get_ss_profile_viewed()
    ss_signin_failure = get_ss_signin_failure()
    #ss_client_latency_perc50 = get_ss_client_latency()

    selfserv_data = {
        'self_serve_pool_row': self_serve_pool_row
      , 'self_serve_pool_latam': self_serve_pool_latam
      , 'ss_interview_requests_fss_existing': ss_interview_requests_fss_existing
      , 'ss_interview_requests_fss_new': ss_interview_requests_fss_new
      , 'ss_interview_requests_platinum_existing': ss_interview_requests_platinum_existing
      , 'ss_interview_requests_platinum_new': ss_interview_requests_platinum_new
      , 'ss_interviews_happened_fss_existing': ss_interviews_happened_fss_existing
      , 'ss_interviews_happened_fss_new': ss_interviews_happened_fss_new
      , 'ss_interviews_happened_platinum_existing': ss_interviews_happened_platinum_existing
      , 'ss_interviews_happened_platinum_new': ss_interviews_happened_platinum_new
      , 'ss_devs_chosen_fss_existing': ss_devs_chosen_fss_existing
      , 'ss_devs_chosen_fss_new': ss_devs_chosen_fss_new
      , 'ss_devs_chosen_platinum_existing': ss_devs_chosen_platinum_existing
      , 'ss_devs_chosen_platinum_new': ss_devs_chosen_platinum_new
      , 'ss_searches_fss': ss_searches_fss
      , 'ss_searches_platinum': ss_searches_platinum
      , 'ss_profile_viewed_fss': ss_profile_viewed_fss
      , 'ss_profile_viewed_platinum': ss_profile_viewed_platinum
      , 'ss_signin_failure': ss_signin_failure
      #, 'ss_client_latency_perc50': ss_client_latency_perc50
    }
    
    return selfserv_data


def get_matching_data():
    """
    Function to get matching data.
    
    Returns:
        (dict): Containing all the metric names and their data pairs. 
    """
    
    devs_shortlisted_fss_existing, devs_shortlisted_fss_new, devs_shortlisted_platinum_existing, devs_shortlisted_platinum_new = get_devs_shortlisted()
    packets_sent_fss_existing, packets_sent_fss_new, packets_sent_platinum_existing, packets_sent_platinum_new = get_packets_sent()
    ms_interview_requests_fss_existing, ms_interview_requests_fss_new, ms_interview_requests_platinum_existing, ms_interview_requests_platinum_new = get_ms_interview_requests()
    ms_interviews_happened_fss_existing, ms_interviews_happened_fss_new, ms_interviews_happened_platinum_existing, ms_interviews_happened_platinum_new = get_ms_interviews_happened()
    ms_devs_chosen_fss_existing, ms_devs_chosen_fss_new, ms_devs_chosen_platinum_existing, ms_devs_chosen_platinum_new = get_ms_devs_chosen()
    ms_client_latency_perc50 = get_ms_client_latency()

    matching_data = {
        'devs_shortlisted_fss_existing': devs_shortlisted_fss_existing
      , 'devs_shortlisted_fss_new': devs_shortlisted_fss_new
      , 'devs_shortlisted_platinum_existing': devs_shortlisted_platinum_existing
      , 'devs_shortlisted_platinum_new': devs_shortlisted_platinum_new
      , 'packets_sent_fss_existing': packets_sent_fss_existing
      , 'packets_sent_fss_new': packets_sent_fss_new
      , 'packets_sent_platinum_existing': packets_sent_platinum_existing
      , 'packets_sent_platinum_new': packets_sent_platinum_new
      , 'ms_interview_requests_fss_existing': ms_interview_requests_fss_existing
      , 'ms_interview_requests_fss_new': ms_interview_requests_fss_new
      , 'ms_interview_requests_platinum_existing': ms_interview_requests_platinum_existing
      , 'ms_interview_requests_platinum_new': ms_interview_requests_platinum_new  
      , 'ms_interviews_happened_fss_existing': ms_interviews_happened_fss_existing
      , 'ms_interviews_happened_fss_new': ms_interviews_happened_fss_new
      , 'ms_interviews_happened_platinum_existing': ms_interviews_happened_platinum_existing
      , 'ms_interviews_happened_platinum_new': ms_interviews_happened_platinum_new
      , 'ms_devs_chosen_fss_existing': ms_devs_chosen_fss_existing
      , 'ms_devs_chosen_fss_new': ms_devs_chosen_fss_new
      , 'ms_devs_chosen_platinum_existing': ms_devs_chosen_platinum_existing
      , 'ms_devs_chosen_platinum_new': ms_devs_chosen_platinum_new
      , 'ms_client_latency_perc50': ms_client_latency_perc50
    }
    
    return matching_data


def get_supply_data():
    """
    Function to get supply data.
    
    Returns:
        (dict): Containing all the metric names and their data pairs. 
    """
    
    total_signups_row, total_signups_latam = get_total_signups()
    resume_uploaded_row, resume_uploaded_latam = get_resume_uploaded()
    signup_completed_row, signup_completed_latam = get_signup_completed()
    seniority_assessment_taken_row, seniority_assessment_taken_latam = get_seniority_assessment_taken()
    seniority_assessment_drop_off_row, seniority_assessment_drop_off_latam = get_seniority_assessment_drop_off()
    devs_taking_mcqs_row, devs_taking_mcqs_latam = get_devs_taking_mcqs()
    devs_taking_demand_forecasted_row, devs_taking_demand_forecasted_latam = get_devs_taking_demand_forecasted_mcqs()
    mcq_dropoff_row, mcq_dropoff_latam = get_mcq_dropoff()
    devs_passing_mcqs_row, devs_passing_mcqs_latam = get_devs_passing_mcqs()
    devs_passing_demand_forecasted_mcqs_row, devs_passing_demand_forecasted_mcqs_latam = get_devs_passing_demand_forecasted_mcqs()
    devs_taking_acc_row, devs_taking_acc_latam = get_devs_taking_acc()
    acc_dropoff_row, acc_dropoff_latam = get_acc_dropoff()
    devs_passing_acc_row, devs_passing_acc_latam = get_devs_passing_acc()
    devs_vetted_row, devs_vetted_latam = get_devs_vetted()
    p2_portal_logins_row, p2_portal_logins_latam = get_p2_portal_logins()
    resume_updates_row, resume_updates_latam = get_resume_updates()
    p2_taking_mcq_row, p2_taking_mcq_latam = get_p2_taking_mcq()
    p2_passing_mcq_row, p2_passing_mcq_latam = get_p2_passing_mcq()

    supply_data = {
        'total_signups_row': total_signups_row
      , 'total_signups_latam': total_signups_latam
      , 'resume_uploaded_row': resume_uploaded_row
      , 'resume_uploaded_latam': resume_uploaded_latam
      , 'signup_completed_row': signup_completed_row
      , 'signup_completed_latam': signup_completed_latam
      , 'seniority_assessment_taken_row': seniority_assessment_taken_row
      , 'seniority_assessment_taken_latam': seniority_assessment_taken_latam
      , 'seniority_assessment_drop_off_row': seniority_assessment_drop_off_row
      , 'seniority_assessment_drop_off_latam': seniority_assessment_drop_off_latam
      , 'devs_taking_mcqs_row': devs_taking_mcqs_row
      , 'devs_taking_mcqs_latam': devs_taking_mcqs_latam
      , 'devs_taking_demand_forecasted_row': devs_taking_demand_forecasted_row
      , 'devs_taking_demand_forecasted_latam': devs_taking_demand_forecasted_latam
      , 'mcq_dropoff_row': mcq_dropoff_row
      , 'mcq_dropoff_latam': mcq_dropoff_latam
      , 'devs_passing_mcqs_row': devs_passing_mcqs_row
      , 'devs_passing_mcqs_latam': devs_passing_mcqs_latam
      , 'devs_passing_demand_forecasted_mcqs_row': devs_passing_demand_forecasted_mcqs_row
      , 'devs_passing_demand_forecasted_mcqs_latam': devs_passing_demand_forecasted_mcqs_latam
      , 'devs_taking_acc_row': devs_taking_acc_row
      , 'devs_taking_acc_latam': devs_taking_acc_latam
      , 'acc_dropoff_row': acc_dropoff_row
      , 'acc_dropoff_latam': acc_dropoff_latam
      , 'devs_passing_acc_row': devs_passing_acc_row
      , 'devs_passing_acc_latam': devs_passing_acc_latam
      , 'devs_vetted_row': devs_vetted_row
      , 'devs_vetted_latam': devs_vetted_latam
      , 'p2_portal_logins_row': p2_portal_logins_row
      , 'p2_portal_logins_latam': p2_portal_logins_latam
      , 'resume_updates_row': resume_updates_row
      , 'resume_updates_latam': resume_updates_latam
      , 'p2_taking_mcq_row': p2_taking_mcq_row
      , 'p2_taking_mcq_latam': p2_taking_mcq_latam
      , 'p2_passing_mcq_row': p2_passing_mcq_row
      , 'p2_passing_mcq_latam': p2_passing_mcq_latam
    }
    
    return supply_data
    

def get_total_signups():
    """
    Function to get number of devs who signed up for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        total_signups_query = (open('Queries/total_signups_query.sql', 'r').read()).format(geography)
        total_signups = query_result(total_signups_query)
        total_signups = data_preprocess(total_signups)
        data.append(total_signups)
    
    return data[0], data[1]


def get_resume_uploaded():
    """
    Function to get number of devs who uploaded resume for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        resume_uploaded_query = (open('Queries/resume_uploaded_query.sql', 'r').read()).format(geography)
        resume_uploaded = query_result(resume_uploaded_query)
        resume_uploaded = data_preprocess(resume_uploaded)
        data.append(resume_uploaded)
    
    return data[0], data[1]


def get_signup_completed():
    """
    Function to get number of devs who completed basic info page for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        signup_completed_query = (open('Queries/signup_completed_query.sql', 'r').read()).format(geography)
        signup_completed = query_result(signup_completed_query)
        signup_completed = data_preprocess(signup_completed)
        data.append(signup_completed)
    
    return data[0], data[1]


def get_seniority_assessment_taken():
    """
    Function to get number of devs who took seniority assessment test for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        seniority_assessment_taken_query = (open('Queries/seniority_assessment_taken_query.sql', 'r').read()).format(geography)
        seniority_assessment_taken = query_result(seniority_assessment_taken_query)
        seniority_assessment_taken = data_preprocess(seniority_assessment_taken)
        data.append(seniority_assessment_taken)
    
    return data[0], data[1]


def get_seniority_assessment_drop_off():
    """
    Function to get number of devs who dropped off after starting seniority assessment test for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        seniority_assessment_drop_off_query = (open('Queries/seniority_assessment_drop_off_query.sql', 'r').read()).format(geography)
        seniority_assessment_drop_off = query_result(seniority_assessment_drop_off_query)
        seniority_assessment_drop_off = data_preprocess(seniority_assessment_drop_off)
        data.append(seniority_assessment_drop_off)
    
    return data[0], data[1]


def get_devs_taking_mcqs():
    """
    Function to get number of devs who are taking technical mcqs for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        devs_taking_mcqs_query = (open('Queries/devs_taking_mcqs_query.sql', 'r').read()).format(geography)
        devs_taking_mcqs = query_result(devs_taking_mcqs_query)
        devs_taking_mcqs = data_preprocess(devs_taking_mcqs)
        data.append(devs_taking_mcqs)
    
    return data[0], data[1]


def get_devs_taking_demand_forecasted_mcqs():
    """
    Function to get number of devs who are taking mcqs for skills which are expected to be in demand for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        devs_taking_demand_forecasted_mcqs_query = (open('Queries/devs_taking_demand_forecasted_mcqs_query.sql', 'r').read()).format(geography)
        devs_taking_demand_forecasted_mcqs = query_result(devs_taking_demand_forecasted_mcqs_query)
        devs_taking_demand_forecasted_mcqs = data_preprocess(devs_taking_demand_forecasted_mcqs)
        data.append(devs_taking_demand_forecasted_mcqs)
    
    return data[0], data[1]


def get_mcq_dropoff():
    """
    Function to get number of devs who are dropping off during mcqs for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        mcq_dropoff_query = (open('Queries/mcq_dropoff_query.sql', 'r').read()).format(geography)
        mcq_dropoff = query_result(mcq_dropoff_query)
        mcq_dropoff = data_preprocess(mcq_dropoff)
        data.append(mcq_dropoff)
    
    return data[0], data[1]


def get_devs_passing_mcqs():
    """
    Function to get number of devs who are passing technical mcqs for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        devs_passing_mcqs_query = (open('Queries/devs_passing_mcqs_query.sql', 'r').read()).format(geography)
        devs_passing_mcqs = query_result(devs_passing_mcqs_query)
        devs_passing_mcqs = data_preprocess(devs_passing_mcqs)
        data.append(devs_passing_mcqs)
    
    return data[0], data[1]


def get_devs_passing_demand_forecasted_mcqs():
    """
    Function to get number of devs who are passing mcqs for skills which are expected to be in demand for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        devs_passing_demand_forecasted_mcqs_query = (open('Queries/devs_passing_demand_forecasted_mcqs_query.sql', 'r').read()).format(geography)
        devs_passing_demand_forecasted_mcqs = query_result(devs_passing_demand_forecasted_mcqs_query)
        devs_passing_demand_forecasted_mcqs = data_preprocess(devs_passing_demand_forecasted_mcqs)
        data.append(devs_passing_demand_forecasted_mcqs)
    
    return data[0], data[1]


def get_devs_taking_acc():
    """
    Function to get number of devs who are taking accs for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        devs_taking_acc_query = (open('Queries/devs_taking_acc_query.sql', 'r').read()).format(geography)
        devs_taking_acc = query_result(devs_taking_acc_query)
        devs_taking_acc = data_preprocess(devs_taking_acc)
        data.append(devs_taking_acc)
    
    return data[0], data[1]


def get_acc_dropoff():
    """
    Function to get number of devs who are dropping off during accs for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        acc_dropoff_query = (open('Queries/acc_dropoff_query.sql', 'r').read()).format(geography)
        acc_dropoff = query_result(acc_dropoff_query)
        acc_dropoff = data_preprocess(acc_dropoff)
        data.append(acc_dropoff)
    
    return data[0], data[1]


def get_devs_passing_acc():
    """
    Function to get number of devs who are passing accs for ROW and LATAM separately.    
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        devs_passing_acc_query = (open('Queries/devs_passing_acc_query.sql', 'r').read()).format(geography)
        devs_passing_acc = query_result(devs_passing_acc_query)
        devs_passing_acc = data_preprocess(devs_passing_acc)
        data.append(devs_passing_acc)
    
    return data[0], data[1]


def get_devs_vetted():
    """
    Function to get number of vetted devs data for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        devs_vetted_query = (open('Queries/devs_vetted_query.sql', 'r').read()).format(geography)
        devs_vetted = query_result(devs_vetted_query)
        devs_vetted = data_preprocess(devs_vetted)
        data.append(devs_vetted)
    
    return data[0], data[1]


def get_p2_portal_logins():
    """
    Function to get number of P2 Portal Logins for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        p2_portal_logins_query = (open('Queries/p2_portal_logins_query.sql', 'r').read()).format(geography)
        p2_portal_logins = query_result(p2_portal_logins_query)
        p2_portal_logins = data_preprocess(p2_portal_logins)
        data.append(p2_portal_logins)
    
    return data[0], data[1]


def get_resume_updates():
    """
    Function to get number of resume updates for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        resume_updates_query = (open('Queries/resume_updates_query.sql', 'r').read()).format(geography)
        resume_updates = query_result(resume_updates_query)
        resume_updates = data_preprocess(resume_updates)
        data.append(resume_updates)
    
    return data[0], data[1]


def get_self_serve_pool():
    """
    Function to get number of devs in the self serve pool for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        self_serve_pool_query = (open('Queries/self_serve_pool_query.sql', 'r').read()).format(geography)
        self_serve_pool = query_result(self_serve_pool_query)
        self_serve_pool = data_preprocess(self_serve_pool)
        data.append(self_serve_pool)
    
    return data[0], data[1]


def get_p2_taking_mcq():
    """
    Function to get number of P2 devs taking technical mcqs for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        p2_taking_mcq_query = (open('Queries/p2_taking_mcq_query.sql', 'r').read()).format(geography)
        p2_taking_mcq = query_result(p2_taking_mcq_query)
        p2_taking_mcq = data_preprocess(p2_taking_mcq)
        data.append(p2_taking_mcq)
    
    return data[0], data[1]


def get_p2_passing_mcq():
    """
    Function to get number of P2 devs passing technical mcqs for ROW and LATAM separately.  
    """
    
    data = []
    for geography in ['ROW', 'LATAM']:
        p2_passing_mcq_query = (open('Queries/p2_passing_mcq_query.sql', 'r').read()).format(geography)
        p2_passing_mcq = query_result(p2_passing_mcq_query)
        p2_passing_mcq = data_preprocess(p2_passing_mcq)
        data.append(p2_passing_mcq)
    
    return data[0], data[1]


def get_devs_shortlisted():
    """
    Function to get number of devs shortlisted for different client category and client types.  
    """
    
    data = []
    for client_category in ['FSS', 'Platinum']:
        for client_type in ['existing', 'new']:
            devs_shortlisted_query = (open('Queries/devs_shortlisted_query.sql', 'r').read()).format(client_category, client_type)
            devs_shortlisted = query_result(devs_shortlisted_query)
            devs_shortlisted = data_preprocess(devs_shortlisted)
            data.append(devs_shortlisted)
    
    return data[0], data[1], data[2], data[3]


def get_packets_sent():
    """
    Function to get number of packets sent for different client category and client types.  
    """
    
    data = []
    for client_category in ['FSS', 'Platinum']:
        for client_type in ['existing', 'new']:
            packets_sent_query = (open('Queries/packets_sent_query.sql', 'r').read()).format(client_category, client_type)
            packets_sent = query_result(packets_sent_query)
            packets_sent = data_preprocess(packets_sent)
            data.append(packets_sent)
    
    return data[0], data[1], data[2], data[3]


def get_ms_interview_requests():
    """
    Function to get number of matching interview requests for different client category and client types.  
    """
    
    data = []
    for client_category in ['FSS', 'Platinum']:
        for client_type in ['existing', 'new']:
            ms_interview_requests_query = (open('Queries/ms_interview_requests_query.sql', 'r').read()).format(client_category, client_type)
            ms_interview_requests = query_result(ms_interview_requests_query)
            ms_interview_requests = data_preprocess(ms_interview_requests)
            data.append(ms_interview_requests)
    
    return data[0], data[1], data[2], data[3]


def get_ss_interview_requests():
    """
    Function to get number of SS interview requests for different client category and client types.   
    """
    
    data = []
    for client_category in ['FSS', 'Platinum']:
        for client_type in ['existing', 'new']:
            ss_interview_requests_query = (open('Queries/ss_interview_requests_query.sql', 'r').read()).format(client_category, client_type)
            ss_interview_requests = query_result(ss_interview_requests_query)
            ss_interview_requests = data_preprocess(ss_interview_requests)
            data.append(ss_interview_requests)
    
    return data[0], data[1], data[2], data[3]


def get_ms_interviews_happened():
    """
    Function to get number of matching interviews happened for different client category and client types.   
    """
    
    data = []
    for client_category in ['FSS', 'Platinum']:
        for client_type in ['existing', 'new']:
            ms_interviews_happened_query = (open('Queries/ms_interviews_happened_query.sql', 'r').read()).format(client_category, client_type)
            ms_interviews_happened = query_result(ms_interviews_happened_query)
            ms_interviews_happened = data_preprocess(ms_interviews_happened)
            data.append(ms_interviews_happened)
    
    return data[0], data[1], data[2], data[3]


def get_ss_interviews_happened():
    """
    Function to get number of SS interview happened for different client category and client types.   
    """
    
    data = []
    for client_category in ['FSS', 'Platinum']:
        for client_type in ['existing', 'new']:
            ss_interviews_happened_query = (open('Queries/ss_interviews_happened_query.sql', 'r').read()).format(client_category, client_type)
            ss_interviews_happened = query_result(ss_interviews_happened_query)
            ss_interviews_happened = data_preprocess(ss_interviews_happened)
            data.append(ss_interviews_happened)
    
    return data[0], data[1], data[2], data[3]


def get_ms_devs_chosen():
    """
    Function to get number of matching devs chosen for different client category and client types.  
    """
    
    data = []
    for client_category in ['FSS', 'Platinum']:
        for client_type in ['existing', 'new']:
            ms_devs_chosen_query = (open('Queries/ms_devs_chosen_query.sql', 'r').read()).format(client_category, client_type)
            ms_devs_chosen = query_result(ms_devs_chosen_query)
            ms_devs_chosen = data_preprocess(ms_devs_chosen)
            data.append(ms_devs_chosen)
    
    return data[0], data[1], data[2], data[3]


def get_ss_devs_chosen():
    """
    Function to get number of SS devs chosen for different client category and client types.  
    """
    
    data = []
    for client_category in ['FSS', 'Platinum']:
        for client_type in ['existing', 'new']:
            ss_devs_chosen_query = (open('Queries/ss_devs_chosen_query.sql', 'r').read()).format(client_category, client_type)
            ss_devs_chosen = query_result(ss_devs_chosen_query)
            ss_devs_chosen = data_preprocess(ss_devs_chosen)
            data.append(ss_devs_chosen)
    
    return data[0], data[1], data[2], data[3]


def get_ss_searches():
    """
    Function to get number of SS search queries for different client category. 
    """
    
    data = []
    for client_category in ['FSS', 'Platinum']:
        ss_searches_query = (open('Queries/ss_searches_query.sql', 'r').read()).format(client_category)
        ss_searches = query_result(ss_searches_query)
        ss_searches = data_preprocess(ss_searches)
        data.append(ss_searches)
    
    return data[0], data[1]


def get_ss_profile_viewed():
    """
    Function to get number of SS profile views for different client category. 
    """
    
    data = []
    for client_category in ['FSS', 'Platinum']:
        ss_profile_viewed_query = (open('Queries/ss_profile_viewed_query.sql', 'r').read()).format(client_category)
        ss_profile_viewed = query_result(ss_profile_viewed_query)
        ss_profile_viewed = data_preprocess(ss_profile_viewed)
        data.append(ss_profile_viewed)
    
    return data[0], data[1]


def get_ss_signin_failure():
    """
    Function to get number of SS sign in failures percentage. 
    """
    
    data = []
    ss_signin_failure_query = open('Queries/ss_signin_failure_query.sql', 'r').read()
    ss_signin_failure = query_result(ss_signin_failure_query)
    ss_signin_failure = data_preprocess(ss_signin_failure)
    data.append(ss_signin_failure)
    
    return data[0]


def get_ss_client_latency():
    """
    Function to get number of SS client latency.  
    """
    
    data = []
    ss_client_latency_query = open('Queries/ss_client_latency_query.sql', 'r').read()
    ss_client_latency = query_result(ss_client_latency_query)
    ss_client_latency = data_preprocess(ss_client_latency)
    data.append(ss_client_latency)
    
    return data[0]


def get_ms_client_latency():
    """
    Function to get number of matching client latency.  
    """
    
    data = []
    ms_client_latency_query = open('Queries/ms_client_latency_query.sql', 'r').read()
    ms_client_latency = query_result(ms_client_latency_query)
    ms_client_latency = data_preprocess(ms_client_latency)
    data.append(ms_client_latency)
    
    return data[0]