import streamlit as st

def app():

    contact_form = """
      <form target="_blank" action="https://formsubmit.co/chriver68@gmail.com" method="POST">
        <div class="form-group">
          <div class="form-row">
            <div class="col">
              <input type="text" name="name" class="form-control" placeholder="Full Name" required>
            </div>
            <div class="col">
              <input type="email" name="email" class="form-control" placeholder="Email Address" required>
            </div>
          </div>
        </div>
        <div class="form-group">
          <textarea placeholder="Your Message" class="form-control" name="message" rows="10" required></textarea>
        </div>
        <button type="submit" class="btn btn-lg btn-dark btn-block">Submit Form</button>
      </form>
    """
    col1, col2, col3= st.columns([1,2,1])
    col2.title(':mailbox: Questions? Suggestions? Message me!')

    col4, col5, col6 = st.columns([2, 1, 3])
    col5.markdown(contact_form, unsafe_allow_html=True)

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    local_css("style/style.css")