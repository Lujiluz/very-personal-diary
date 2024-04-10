$(function () {
  getDiary();
  bsCustomFileInput.init();
});

const getDiary = () => {
  $.ajax({
    type: 'GET',
    url: '/diary',
    data: {},
    success: function (res) {
      res.diaries.map((diary) => {
        let temp = `<div class="col-4 my-2">
          <div class="card">
            <img src="../static/${diary.image || 'default-img.jpg'}" alt="..." class="card-img-top" />
            <div class="card-body">
            <div class="mb-3 mt-1">
              <p class="d-inline text-muted">emotion: </p>
              <img src="../static/${diary.emotion || 'default-emotion.jpg'}" alt="..." class="profile-img card-img-top m-1" />
            </div>
              <h5 class="card-title">${diary.title}</h5>
              <p class="card-text">${diary.description}</p>
              <h6 class="card-subtitle mb-2 text-muted">${diary.date}</h6>
            </div>
          </div>
        </div>`;

        $('#cards-box').append(temp);
      });
    },
  });
};

const postDiary = () => {
  let title = $('#title').val();
  let description = $('#description').val();
  let image = $('#image').prop('files')[0];
  let emotion = $('#emotion').prop('files')[0];

  if (title === '' || description === '') return alert('Please complete the form!');
  form_data = new FormData();
  form_data.append('image', image);
  form_data.append('emotion', emotion);
  form_data.append('title', title);
  form_data.append('description', description);
  $.ajax({
    type: 'POST',
    url: '/diary',
    data: form_data,
    contentType: false,
    processData: false,
    success: function (res) {
      alert(res.msg);
      window.location.reload();
    },
  });
};

const handleClearAllDiaries = () => {
  if (confirm('are you sure to delete all diaries?')) {
    $.ajax({
      type: 'DELETE',
      url: '/diary',
      data: {},
      success: function (res) {
        alert(res.msg);
        window.location.reload();
      },
    });
  }
};
