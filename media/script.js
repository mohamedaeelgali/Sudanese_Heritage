
//selecting all required elements
const dropArea = document.querySelector(".drag-area"),
  dragText = dropArea.querySelector("header"),
  // button = dropArea.querySelector("button"),
  input = dropArea.querySelector("input")
let file //this is a global variable and we'll use it inside multiple functions
const button = document.getElementById("btn")
//const imageRight = document.getElementById("img-right")
const upload = document.getElementById("upload")
const uploadText = document.getElementById("upload-text")
//const translateArabBtn = document.getElementById("translate-arab")
const translateEngBtn = document.getElementById("translate-eng")
const description = document.getElementById("description")
//const texts = document.getElementById("texts")

//texts.style.display = "none"

button.onclick = () => {
  input.click() //if user click on the button then the input also clicked
}
upload.onclick = () => {
  if (!fileURL) {
    alert("Please browse an image first")
  } else {
   // imageRight.src = fileURL
   // imageRight.style.display = "inline"
   // texts.style.display = "inline"
  }
}

input.addEventListener("change", function () {
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
document.querySelector('#btn').files= this.files
  file = this.files[0]
  dropArea.classList.add("active")
  showFile() //calling function
})


//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event) => {
  event.preventDefault() //preventing from default behaviour
  dropArea.classList.add("active")
  dragText.textContent = "Release to Upload File"
})
//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("active")
  dragText.textContent = "Drag & Drop to Upload File"
})
//If user drop File on DropArea
dropArea.addEventListener("drop", (event) => {
  event.preventDefault() //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0]
document.querySelector('#btn').files=event.dataTransfer.files
  showFile() //calling function
})

function showFile() {
  let fileType = file.type //getting selected file type
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"] //adding some valid image extensions in array
  if (validExtensions.includes(fileType)) {
    //if user selected file is an image file
    let fileReader = new FileReader() //creating new FileReader object
    fileReader.onload = () => {
      fileURL = fileReader.result //passing user file source in fileURL variable
      // UNCOMMENT THIS BELOW LINE. I GOT AN ERROR WHILE UPLOADING THIS POST SO I COMMENTED IT
      let imgTag = `<img src="${fileURL}" alt="image">` //creating an img tag and passing user selected file source inside src attribute
      dropArea.innerHTML = imgTag //adding that created img tag inside dropArea container
      console.log(fileURL)
    }
    fileReader.readAsDataURL(file)
  } else {
    alert("This is not an Image File!")
    dropArea.classList.remove("active")
    dragText.textContent = "Drag & Drop to Upload File"
  }
}


