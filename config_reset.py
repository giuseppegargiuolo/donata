import _config_generatedatabase as generatedatabase
import _config_migrate as migrate
import _config_seed as seed
import _config_fakeusers as users

### Main ###########################
if __name__ == '__main__':
    generatedatabase.main()
    migrate.main()
    seed.main()
    users.main()