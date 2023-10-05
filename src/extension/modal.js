export const modalHtml = `
  <div class="modal-custom-edit">
    <div class="modal-content">
      <span class="close-modal">&times;</span>
      <h2>Modal Form</h2>
      <form class="modal-form">
        <input type="text" name="subject-name" placeholder="Name" />
        <button type="submit" class="submit-edit-modal">Submit</button>
      </form>
    </div>
  </div>
  `
;


// Create the CSS styles for the modal form
export const modalCss = `
  .modal-custom-edit {
    display: none;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.4);
  }

  .modal-content {
    background-color: #fefefe;
    margin: 0 auto;
    margin-top: 10%;
    max-width: 400px;
    padding: 20px;
    border: 1px solid #888;
  }

  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
  }
  
  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
`;