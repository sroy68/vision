def approve(feature_name):
    ans = input(f"Approve feature '{feature_name}'? (YES/NO): ")
    return ans.strip().upper() == "YES"
