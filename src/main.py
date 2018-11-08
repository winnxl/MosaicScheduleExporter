# Placeholder
import connector

c = connector.CalUpload()
c.login()
# print(c.create_cal()) # Prints ID of newly created calendar
c.push_to_schedule()
input("press key to remove and logout...")
c.remove_new_cal()
c.logout()



#c.logout()