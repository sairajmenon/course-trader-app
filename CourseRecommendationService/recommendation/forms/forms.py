from recommendation.model.models import User
from recommendation.exceptions import UserNameValidationError,EmailDoesNotExist,EmailAndPasswordDoNotMatch,EmailValidationError



class Validations:
    def validate_username_email(self,username,email):
        return self.validate_username(username) and self.validate_email(email)


formString = """
    <style>
        h1 {
            color: green;
        }
        
        .multipleSelection {
            width: 300px;
        background-color: #BCC2C1;
        }
        
        .selectBox {
            position: relative;
        }
        
        .selectBox select {
            width: 100%;
        font-weight: bold;
        }
        
        .overSelect {
            position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        }
        
        #checkBoxes {
        display: none;
        border: 1px #8DF5E4 solid;
        }
        
        #checkBoxes label {
        display: block;
        }
        
        #checkBoxes label:hover {
        background-color: #4F615E;
        }
    </style>
    <div>
        <form method='POST' action=''>
            <fieldset class='form-group'>
                <legend class='border-bottom mb-4'>Get Recommendation</legend>  
              <label for="fname">Major</label><br>
              <select name="major" id="major">
                  <option value="volvo">Computer Science</option>
                  <option value="saab">Computer Engineering</option>
              </select><br/><br/>
              <label for="fname">Specialization</label><br/>
              <select name="major" id="major">
                  <option value="1">MS-Non-Thesis</option>
                  <option value="2">MS-Thesis</option>
                  <option value="3">MS-Cybersecurity</option>
                  <option value="4">MS-Biomedical Informatics</option>
                  <option value="5">MS-Arts, Media, and Engineering</option> 
                  <option value="5">MS-Big Data Systems Concentration</option>
              </select><br/><br/>
              <label for="fname">Interests</label><br/>
              <div class="multipleSelection">
                  <div class="selectBox"
                    onclick="showCheckboxes()">
                    <select>
                      <option>Select options</option>
                    </select>
                    <div class="overSelect"></div>
                  </div>
                  <div id="checkBoxes">
                    <label for="first"><input type="checkbox" id="first" /> Databases</label>
                    <label for="second"><input type="checkbox" id="second" />
                      Operating Systems
                    </label>
                    <label for="third">
                      <input type="checkbox" id="third" />
                      Cloud and Distributed systems
                    </label>
                    <label for="fourth">
                      <input type="checkbox" id="fourth" />
                      Artificial Intelligence
                    </label>
                    <label for="fourth">
                      <input type="checkbox" id="fourth" />
                      Machine Learning
                    </label>
                    <label for="fourth">
                      <input type="checkbox" id="fourth" />
                      Natural Language Processing
                    </label>
                  </div>
                </div>
              
                <div class='form-group'>
                    <button type='submit' class='btn btn-primary'>Submit</button>
                </div>
            </fieldset>
        </form>
</div>
<script>
        var show = true;
        
        function showCheckboxes() {
            var checkboxes = \
        document.getElementById("checkBoxes");
        
        if (show) {
            checkboxes.style.display = "block";
        show = false;
        } else {
            checkboxes.style.display = "none";
        show = true;
        }
        }
</script>
"""


