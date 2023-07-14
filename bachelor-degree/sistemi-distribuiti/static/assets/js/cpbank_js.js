/* ####################################################################################################################
CPBANK JS DOCUMENT
#################################################################################################################### */
// Some optimization could be made for alerts managements. //


// Global variables, useful for avoiding too many ajax requests

var accountsActive = [];
var accountsInactive = [];

var currentTable = "";
var currentSearch = [];

var result;

var copy = false;
var copytext = "";
var doubleUUIDv4Regex = new RegExp("([0-9a-f]{40})");

var chartColors = {
  red: 'rgb(255, 99, 132)',
  green: 'rgb(54, 235, 162)'
};

/* ####################################################################################################################
Functions to retrieve and update the transaction table
#################################################################################################################### */

function submitFormAccount() {
  getAccountInfo($("#id").val());
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Ajax request to get the account info (transactions), table initialization, chart rendering.
function getAccountInfo(str) {

  // Check if current loaded table's id is the same as the one to search. If so, don't do the ajax request. 
  if (currentTable !== str) {
    currentTable = str;
    $("#id").val(str);

    // Ajax request
    $.getJSON("/api/account/" + str)

      .done(function (data) {

        // hide data to update
        $("#userData").fadeOut(200);
        $("#alert").hide();

        $("#account").text(data.name + " " + data.surname + ": " + data.balance);

        // Table string
        let t = '';

        // Chart data
        let labels = [];
        let values = [];

        $(data.operations).each(function (index, item) {

          // Save transaction data in local variables for better readability
          let uuidv4 = item[0];

          let currentId = $("#id").val();
          let idSender = item[1].idSender;
          let idRecipient = item[1].idRecipient;

          let isSenderActive = item[1].senderIsActive;
          let isRecipientActive = item[1].recipientIsActive;
          let opType = item[1].type;

          let amount = item[1].amount;
          let floatAmount = parseFloat(item[1].amount.replaceAll('$', ''));
          if (!(item[1].amount == 0 ||
            item[1].idSender == item[1].idRecipient ||
            item[1].type == 1 ||
            (item[1].idRecipient == $("#id").val() && (item[1].type == 0 || item[1].type == 3 || item[1].type == 4)))) {
            floatAmount = -floatAmount;
          }

          let date = new Date(item[1].date);
          let formattedDate = formatDate(date);
          let formattedDay = formattedDate.substring(0, 10);

          let count = labels.length;

          // Generate values for the chart
          if (opType < 3) {
            if (count !== 0 && labels[count - 1] === formattedDay) {
              values[count - 1] = Math.round(values[count - 1] + floatAmount);
            }
            else {
              labels.push(formattedDay);
              values.push(floatAmount);
            }}

          // Begin table, set to bold if it is latest operation
          if (index == (data.operations.length - 1)) {
            t += '<tr style="font-weight: bold">';
          }
          else {
            t += '<tr>';
          }
          
          // Set table row, with styles
          t += '<td>' + uuidv4 + '</td>';

          t += '<td>' + stringOpType(opType) + '</td>';
          if (isSenderActive) {
            t += '<td onclick=\"getAccountInfo(\'' + idSender + '\')\">' + idSender + '</td>';
          }
          else {
            t += '<td style=\"color: #aaaaaa\">' + idSender + '</td>';
          }

          if (idRecipient == null) {
            t += '<td>' + "(Done through API)" + '</td>';
          }
          else if (isRecipientActive) {
            t += '<td onclick=\"getAccountInfo(\'' + idRecipient + '\')\">' + idRecipient + '</td>';
          }
          else { { t += '<td style=\"color: #aaaaaa\">' + idRecipient + '</td>'; } }

          if (floatAmount == 0 || idSender == idRecipient) {
            t += '<td>' + amount + '</td>';
          } else {
            switch (opType) {
              case 0:
                if (floatAmount > 0) t += '<td class="green">' + amount + '</td>';
                else t += '<td class="red">-' + amount + '</td>';
                break;
              case 1:
                t += '<td class="green">' + amount + '</td>';
                break;
              case 2:
                t += '<td class="red">-' + amount + '</td>';
                break;
              case 3:
              case 4:
                if (floatAmount > 0) t += '<td class="blue">' + amount + '</td>';
                else t += '<td class="blue">-' + amount + '</td>';
                break;
            }
          }

          t += '<td>' + formattedDate + '</td>';

          t += '</tr>';
        });

        // Wait and show new data
        setTimeout(function () {
          $("#info").html(t);
          $("#userData").fadeIn(200);
        }, 200);

        // Render chart
        renderBarChart(values, labels);
        renderLineChart(values, labels);
      })

      // If the request fails, print the error
      .fail(function (xhr, status, error) {
        $("#account").text("Enter the id to get the \"owner\"");
        $("#userData").hide();
        $("#alert").removeClass("alert-success");
        $("#alert").addClass("alert-danger");
        $("#alertMsg").html("<strong>Error " + xhr.status + ": </strong>" + JSON.parse(xhr.responseText).content);
        $("#alert").fadeIn(300);
        $("#alert").delay(5000).fadeOut(300);
      });
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function stringOpType(n) {
  switch (n) {
    case 0: return "Transfer";
    case 1: return "Deposit";
    case 2: return "Withdrawal";
    case 3: return "Cancellation";
    case 4: return "Cancelled";
    default: return "Invalid Op Number";
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function formatDate(d) {
  let formatted = "";
  let month = '' + (d.getMonth() + 1);
  let day = '' + d.getDate();
  let year = '' + d.getFullYear();
  let hours = '' + d.getHours();
  let minutes = '' + d.getMinutes();
  let seconds = '' + d.getSeconds();
  let milliseconds = '' + d.getMilliseconds();
  if (month.length < 2)
    month = '0' + month;
  if (day.length < 2)
    day = '0' + day;
  if (hours.length < 2)
    hours = '0' + hours;
  if (minutes.length < 2)
    minutes = '0' + minutes;
  if (seconds.length < 2)
    seconds = '0' + seconds;
  while (milliseconds.length < 3) {
    milliseconds = '0' + milliseconds;
  }
  return day + "/" + month + "/" + year + " " + hours + ":" + minutes + ":" + seconds + "." + milliseconds;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function renderBarChart(values, labels) {
  var chart = document.querySelector('#barChart canvas').chart;

  chart.data.labels = labels;
  chart.data.datasets[0].data = values;
  let dataset = chart.data.datasets[0];
  dataset.backgroundColor = [];
  for (var i = 0; i < dataset.data.length; i++) {
    if (dataset.data[i] > 0) dataset.backgroundColor[i] = chartColors.green;
    else dataset.backgroundColor[i] = chartColors.red;
  }
  chart.update();
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function renderLineChart(values, labels) {
  var chart = document.querySelector('#lineChart canvas').chart;
  var newValues = [];
  newValues[0] = values[0];
  for (var i = 1; i < values.length; i++) {
    newValues[i] = newValues[i - 1] + values[i];
  }
  chart.data.labels = labels;
  chart.data.datasets[0].data = newValues;
  chart.update();
}



/* ####################################################################################################################
Functions to transfer money or divert an operation
#################################################################################################################### */

// Transfer money
function transfer(form) {
  $.post("/api/transfer",
    { from: $("#senderId").val(), to: $("#recipientId").val(), amount: $("#amount").val() })
    .done(function (data) {
      $("#alert4").addClass("alert-success");
      $("#alert4").removeClass("alert-danger");
      $("#alertMsg4").html("Transaction <strong>" + data.id + "</strong> successful");
      $("#alert4").fadeIn(300);
      $("#alert4").delay(5000).fadeOut(300);

    })

    .fail(function (xhr, status, error) {
      $("#alert4").removeClass("alert-success");
      $("#alert4").addClass("alert-danger");
      $("#alertMsg4").html("<strong>Error " + xhr.status + ": </strong>" + JSON.parse(xhr.responseText).content);
      $("#alert4").fadeIn(300);
      $("#alert4").delay(5000).fadeOut(300);
    });
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Divert an operation, gets the uuid from specific component
function divert() {
  $.post("/api/divert",
    { id: $("#uuidv4").val() })
    .done(function (data) {
      $("#alert3").addClass("alert-success");
      $("#alert3").removeClass("alert-danger");
      $("#alertMsg3").html("Transaction <strong>" + $("#uuidv4").val() + "</strong> diverted; cancellation has UUID v4 <strong>" + data.id + "</strong>");
      $("#alert3").fadeIn(300);
      $("#alert3").delay(5000).fadeOut(300);
    })
    .fail(function (xhr, status, error) {
      $("#alert3").removeClass("alert-success");
      $("#alert3").addClass("alert-danger");
      $("#alertMsg3").html("<strong>Error " + xhr.status + ": </strong>" + JSON.parse(xhr.responseText).content);
      $("#alert3").fadeIn(300);
      $("#alert3").delay(5000).fadeOut(300);
    });
}


/* ####################################################################################################################
Functions to get all accounts' table
#################################################################################################################### */

// Function called on submit, saves current search
function submitFormSearchAccount() {
  let surname = $("#accountSurname").val();
  let name = $("#accountName").val();
  var active = ($("#accountType").text() === "Active");

  if (currentSearch[0] != surname ||
    currentSearch[1] != name ||
    currentSearch[2] != active) {
    currentSearch = [surname, name, active];
    getAccounts(surname, name, active);
  }

}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Gets account if not yet saved (gloabl variables accountsInactive and accountsActive), 
// then calls showResult() to filter them
function getAccounts(surname, name, active) {
  currentSearch = [surname, name, active];
  let currentArray = [];
  if (active) currentArray = accountsActive;
  else currentArray = accountsInactive;

  $("#usersData").hide();
  $("#alert2").hide();

  if (active) {
    $("#enable").text("Deactivate");
    $("#enable").addClass("inactiveB");
    $("#enable").removeClass("activeB");
  }
  else {
    $("#enable").text("Activate");
    $("#enable").addClass("activeB");
    $("#enable").removeClass("inactiveB");
  }

  if (currentArray.length === 0) {
    let url = "";
    if (active) url = "/api/account";
    else url = "/api/inactive";
    
    // Ajax request to get account
    $.getJSON(url)
      .done(function (map) {
        for (let key in map) {
          let accountId = key;

          let accountName = map[key].name;
          let accountSurname = map[key].surname;
          let accountBalance = map[key].balance;

          currentArray.push([accountId, accountSurname, accountName, accountBalance]);
        }
        showResult(currentArray, surname, name);
      })

      .fail(function (xhr, status, error) {
        $("#usersData").hide();
        $("#alert2").removeClass("alert-success");
        $("#alert2").addClass("alert-danger");
        $("#alertMsg2").html("<strong>Error " + xhr.status + ": </strong>" + JSON.parse(xhr.responseText).content);
        $("#alert2").fadeIn(300);
        $("#alert2").delay(5000).fadeOut(300);
      });
  }
  else showResult(currentArray, surname, name);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Filter the accounts by name and surname and display them
function showResult(currentArray, surname, name) {
  let t = "";
  

  currentArray.forEach(function (account) {
    if ((account[2].toLowerCase().includes(name.toLowerCase()) &&
      account[1].toLowerCase().includes(surname.toLowerCase())) ||
      (surname === "" && name === "")) {

      let arrStr = `['${account[0]}', '${account[1]}', '${account[2]}', '${account[3]}']`;

      t += '<tr onclick="select(' + arrStr + ')">';

      for (let j = 0; j < 4; j++)  t += '<td>' + account[j] + '</td>';

      t += '</tr>';
    }
  });

  setTimeout(function () {
    if (t !== "") {
      $("#infoAccounts").html(t);
      $("#usersData").fadeIn(200);
    } else {
      $("#alert2").removeClass("alert-success");
      $("#alert2").addClass("alert-danger");
      $("#alertMsg2").html("<strong>Error: </strong>no matching result found");
      $("#alert2").fadeIn(300);
      $("#alert2").delay(5000).fadeOut(300);
    }
  }, 200);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// toggle the button to search for active or inactive accounts
function toggleActive() {
  if ($("#accountType").text() === "Active") $("#accountType").text("Inactive");
  else $("#accountType").text("Active");
  $("#accountType").toggleClass("activeB");
  $("#accountType").toggleClass("inactiveB");
}

/* ####################################################################################################################
Functions to manage modify-delete-create accounts forms
#################################################################################################################### */

// clean form
function cleanChangeForm() {
  $("#selectedId").text("Select id...");
  $("#selectedSurname").val("");
  $("#selectedName").val("");
  $("#save").attr("disabled");
  $("#enable").attr("disabled");
  $("#save").addClass("disabled");
  $("#enable").addClass("disabled");
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// clean form
function cleanCreateForm() {
  $("#newSurname").val("");
  $("#newName").val("");
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// select account to modify, enter info in the form
function select(account) {
  if (copy) {
    updateCopytext(account[0]);
  }
  $("#selectedId").text(account[0]);
  $("#selectedSurname").val(account[1]);
  $("#selectedName").val(account[2]);
  if (currentSearch[2]) {
    $("#save").removeAttr("disabled");
    $("#save").removeClass("disabled");
  }
  $("#enable").removeAttr("disabled");
  $("#enable").removeClass("disabled");
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Delete an active account or enable an inactive one
function enableOrDelete() {
  let url = "/api/account?id=" + $("#selectedId").text();
  let htmlMsg = "<strong>Done: </strong>Account deleted. Updating table and showing inactive accounts...";

  if ($("#enable").text() === "Activate") {
    url = '/api/inactive?id=' + $("#selectedId").text();
    htmlMsg = "<strong>Done: </strong>Account activated. Updating table and showing active accounts...";
  }

  $.ajax({
    url: url,
    type: 'DELETE',
    success: function (result) {
      $("#alert2").addClass("alert-success");
      $("#alert2").removeClass("alert-danger");
      $("#alertMsg2").html(htmlMsg);
      $("#alert2").fadeIn(250);
      $("#alert2").delay(3000).fadeOut(250);
      cleanChangeForm();
      setTimeout(function () {
        accountsActive = [];
        accountsInactive = [];
        currentSearch[2] = !currentSearch[2];
        toggleActive();
        getAccounts(currentSearch[0], currentSearch[1], currentSearch[2]);
      }, 3500);
    },
    error: function (xhr, status, error) {
      $("#usersData").hide();
      $("#alert2").removeClass("alert-success");
      $("#alert2").addClass("alert-danger");
      $("#alertMsg2").html("<strong>Error " + xhr.status + ": </strong>" + JSON.parse(xhr.responseText).content);
      $("#alert2").fadeIn(300);
      $("#alert2").delay(5000).fadeOut(300);
    }
  });
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Create new account
function createNewAccount() {
  $.post("/api/account",
    { name: $("#newName").val(), surname: $("#newSurname").val() })
    .done(function (data) {
      $("#alert2").addClass("alert-success");
      $("#alert2").removeClass("alert-danger");
      $("#alertMsg2").html("Account created with id <strong>" + data.content + "</strong>; showing all accounts...");
      $("#alert2").fadeIn(250);
      $("#alert2").delay(3000).fadeOut(250);
      setTimeout(function () {
        accountsActive = [];
        accountsInactive = [];
        cleanCreateForm();
        currentSearch = ["", "", true];
        getAccounts(currentSearch[0], currentSearch[1], currentSearch[2]);
      }, 3500);
    })

    .fail(function (xhr, status, error) {
      $("#alert2").removeClass("alert-success");
      $("#alert2").addClass("alert-danger");
      $("#alertMsg2").html("<strong>Error " + xhr.status + ": </strong>" + JSON.parse(xhr.responseText).content);
      $("#alert2").fadeIn(300);
      $("#alert2").delay(5000).fadeOut(300);
    });
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Update name and surname of an existing account
function saveNewData() {
  $.ajax({
    url: '/api/account/' + $("#selectedId").text(),
    type: 'PUT',
    data: "surname=" + $("#selectedSurname").val() + "&name=" + $("#selectedName").val(),
    success: function (result) {
      $("#alert2").addClass("alert-success");
      $("#alert2").removeClass("alert-danger");
      $("#alertMsg2").html("<strong>Done: </strong>Account updated. Updating table...");
      $("#alert2").fadeIn(250);
      $("#alert2").delay(2000).fadeOut(250);
      cleanChangeForm();
      setTimeout(function () {
        accountsActive = [];
        accountsInactive = [];
        getAccounts(currentSearch[0], currentSearch[1], currentSearch[2]);
      }, 2500);
    },
    error: function (xhr, status, error) {
      $("#usersData").hide();
      $("#alert2").removeClass("alert-success");
      $("#alert2").addClass("alert-danger");
      $("#alertMsg2").html("<strong>Error " + xhr.status + ": </strong>" + JSON.parse(xhr.responseText).content);
      $("#alert2").fadeIn(300);
      $("#alert2").delay(5000).fadeOut(300);
    }
  });
}

/* ####################################################################################################################
Functions to do the copy mechanism - BETA
#################################################################################################################### */

// Activate the copy mechanism
function activateCopy() {
  copy = true;
  $("#copy").addClass("activeB");
  copytext = [];
  $("#alert2").addClass("alert-success");
  $("#alert2").removeClass("alert-danger");
  $("#alertMsg2").html("<strong>Copy activated: </strong>Click on two ids, one at a time, to copy them");
  $("#alert2").fadeIn(300);
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Update the string, if done copy to the clipboard
function updateCopytext(id) {
  if (copytext.length === 0) {
    copytext += id;
    $("#alert2").addClass("alert-success");
    $("#alert2").removeClass("alert-danger");
    $("#alertMsg2").html("<strong>Copy activated: </strong>Click on another id to complete the copy");
  }
  else if (copytext.length === 20) {
    copytext += id;
    navigator.clipboard.writeText(copytext);
    $("#alert2").addClass("alert-success");
    $("#alert2").removeClass("alert-danger");
    $("#alertMsg2").html("<strong>Copy done: </strong>Go to the transfer page and click paste to use the copied ids");
    $("#alert2").delay(3000).fadeOut(300);
    copytext = "";
    copy = false;
    $("#copy").removeClass("activeB");
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Paste into the input text in transfer page
function pasteCopytext() {
  navigator.clipboard.readText().then(
    clipText => {
      if (doubleUUIDv4Regex.test(clipText)) {
        $("#senderId").val(clipText.substring(0, 20));
        $("#recipientId").val(clipText.substring(20));
      }
      else {
        $("#alert4").removeClass("alert-success");
        $("#alert4").addClass("alert-danger");
        $("#alertMsg4").html("<strong>Error: </strong>The clipboard content is not valid. Copy two Ids in the <a href=\"/accounts\">Account page</a>");
        $("#alert4").fadeIn(300);
        $("#alert4").delay(3000).fadeOut(300);
      }
    },

    function () {
      $("#alert4").removeClass("alert-success");
      $("#alert4").addClass("alert-danger");
      $("#alertMsg4").html("<strong>Error: </strong>Something is wrong with your ClipboardAPI, or you denied the permission");
      $("#alert4").fadeIn(300);
      $("#alert4").delay(3000).fadeOut(300);
    });
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////*