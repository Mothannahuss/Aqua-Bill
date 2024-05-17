
document.addEventListener('DOMContentLoaded', function () {

    const todayDate = new Date();
    let todaysReading = 0;
    let date_data = getLastSevenDays().reverse();
    let month_data = getLastSixMonths();
    let readings = [0, 0, 0, 0,0];
    const months = getLastSixMonths();
    let home_data = document.querySelector("#content").innerHTML;
    let url = this.location.href.split("/");
    const unit_num = /^[0-9]+$/.test(url[url.length - 1]) ? url[url.length - 1] : null;
    let doWeFetch = unit_num != null ? true : false;
    let changeCounter = 0;
    let lastReading = 0;
    let current_date = new Date();
    let today = current_date.getDate();
    let displayed = false;
    let daily = false;


    assignEvents();
    getDailyArchives();
    displayDateTime();
    pushBillNotification();

    async function pushBillNotification()
    {
        let current_bill = await getBill();
        current_bill = current_bill[0] * 0.25;
        let bill_message = "Your current bill is ";
        let message = "Water bill is due in " + (27 - today) + " days";
        let notifications = document.querySelector("#nots");
        notifications.innerHTML = '';
        let new_item = document.createElement("li");
        new_item.innerHTML = `
            <a id="bill-date" href="#"
                        ><i class="bi bi-app-indicator"></i> ${message}</a
                      >

            <a id="bill" href="#"
                      ><i class="bi bi-app-indicator"></i> ${bill_message} ${current_bill} SAR</a
                    >
            `;

        notifications.appendChild(new_item);
        
    }


    async function getBill()
    {
        if (!unit_num)
        {
                return;
        }

        let response = await fetch("/bill/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({unit:unit_num})
        });

        let data = await response.json();

        return data;

    }


    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: date_data,
            datasets: [{
                label: 'Water Consumed in Liters',
                data: readings,
                backgroundColor: 'white',
                borderColor: 'white',
                borderWidth: 2
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        display: false
                    },
                    border: { display: false },
                    ticks: {
                        color: "#FFFFFF",
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    border: { display: false },
                    ticks: {
                        color: "#FFFFFF",
                    }
                },
            },
            responsive: true,
            maintainAspectRatio: true
        }
    });

    if (doWeFetch) {
        fetchData();
    }



    function pushNotification(message) {
        let notifications = document.querySelector("#nots");
        let isLeaked = false;


        notifications.children.forEach(child => {
            if (child.id == "leak") {
                isLeaked = true;
            }
        })

        if (!isLeaked) {
            let new_item = document.createElement("li");
            new_item.innerHTML = `
            <a id="leak" href="#"
                        ><i class="bi bi-app-indicator"></i> ${message}</a
                      >
            `;

            notifications.appendChild(new_item);
        }
    }


    function getLastSevenDays() {
        const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        const result = [];

        let date = new Date();

        for (let i = 0; i < 5; i++) {
            result.push(daysOfWeek[date.getDay()]);

            date.setDate(date.getDate() - 1);
        }

        return result;
    }


    function getLastSixMonths() {
        const months = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sep", "October", "Nov", "Dec"];
        let month = todayDate.getMonth();
        let diff = month - 6 >= 0 ? month - 6 : 0;

        return months.slice(diff, month+1);
    }


    async function getDailyArchives() {
        readings = [0,0,0,0,0];
        daily = true;

        let response = [];

        let res = await fetch("http://127.0.0.1:8000/daily/", {
            method: "POST",
            body: JSON.stringify({"unit": unit_num})
        });

        response = await res.json();
        data = response.readings;

        if (data.length == 0)
            {
                return;
            }

        data.forEach(day => {
            let reading = day[0];
            let day_name = day[1];

            let index = date_data.indexOf(day_name);

            if (index != -1) {
                readings[index] = reading;
            }
        })

        readings[readings.length - 1] = todaysReading;
        myChart.data.datasets.data= readings;
        myChart.update();
    }

    async function getMonthlyArchives() {
        daily = false;

        readings = [0,0,0,0,0];
        let response = [];

        let res = await fetch("http://127.0.0.1:8000/monthly/", {
            method: "POST",
            body: JSON.stringify({"unit": unit_num})
        });

        response = await res.json();
        data = response.readings;

        if (data.length == 0)
            {
                return;
            }


        indices = []
        data.forEach(month => {
            let reading = month[0];
            let day_name = month[1];
            console.log(reading, day_name);


            let index = month_data.indexOf(day_name);

            if (index != -1) {
                readings[index] = reading;
            }
        })

        
        myChart.data.datasets.data= readings;
        myChart.update();

    }


    function clearChart()
    {

        myChart.data.datasets.forEach((dataset) => {
            dataset.data.clear();
        });
        myChart.update();
    }

    function showChart() {
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: date_data,
                datasets: [{
                    label: 'Water Consumed in Liters',
                    data: readings,
                    backgroundColor: 'white',
                    borderColor: 'white',
                    borderWidth: 2
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            display: false
                        },
                        border: { display: false },
                        ticks: {
                            color: "#FFFFFF",
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        border: { display: false },
                        ticks: {
                            color: "#FFFFFF",
                        }
                    },
                    responsive: true,
                    maintainAspectRatio: false

                },
            }
        });
    }



    setInterval(fetchData, 10000);



    // function displayQuality(quality) {
    //     console.log(quality);
    //     let contaainer = document.querySelector(".progress-bar");
    //     var bar = new ProgressBar.SemiCircle(container, {
    //         strokeWidth: 6,
    //         color: "#618ffb",
    //         trailColor: "#618ffb",
    //         trailWidth: 1,
    //         easing: 'easeInOut',
    //         duration: 1400,
    //         svgStyle: null,
    //         text: {
    //             value: quality + "% of drinkable water",
    //             alignToBottom: true,
    //             style: {
    //                 // Positioning the text at the center
    //                 position: 'absolute',
    //                 left: '50%',
    //                 top: '50%',
    //                 padding: 0,
    //                 margin: 0,
    //                 // Transforming text to be centered
    //                 transform: {
    //                     prefix: true,
    //                     value: 'translate(-30%, -30%)'
    //                 },
    //                 // Setting a contrasting color and increasing size
    //                 color: '#618ffb',
    //                 fontSize: '1em',
    //                 fontFamily: '"Raleway", Helvetica, sans-serif',
    //             }
    //         }
    //     });
    
    //     bar.animate(quality);
    // }
    
    async function fetchData() {
        if (doWeFetch) {
            let res = await fetch("http://127.0.0.1:8000/device/" + unit_num);
            let data = await res.json();

            let readings_card = document.querySelector("#reading");
            let current_reading = readings_card.innerHTML.split(" ")[0];

            if (current_reading != lastReading) {
                changeCounter++;
                lastReading = current_reading;
            }
            else {
                changeCounter = 0;
            }

            if (changeCounter == 6) {
                pushNotification("Possible leakage, please reach out to management");
            }
            readings_card.innerText = data['reading'] + " Liters consumed today";
            document.querySelector("#price").innerText = data['reading'] * 0.25 + " SAR charged today";
            reading[readings.length - 1] += data['reading'];
            

            if (daily)
                {
                    todaysReading = data['reading'];
                    readings[readings.length - 1] = todaysReading;
                    console.log(readings);
                    myChart.update();
                }
            
                
        }
    }
    function displayFeatures() {
        let container = document.querySelector("#content");
        container.innerHTML = '';
        container.innerHTML = `
        <div class="row p-4">
        <div class="card-lg-features" style="margin-right:2%;">
            <h3>Water Consumption Tracking</h3>
            <p>Aquabil can help you to know exactly how much water you consume on daily, monthly or weekly basis.</p>
        </div>
        <div class="card-lg-features">
            <h3>Consumption bill Tracking</h3>
            <p>Aquabil can help you to know exactly how much money your consume will cost you on daily, monthly or weekly basis.</p>
        </div>
        </div>
        <div class="row p-4">
        <div class="card-lg-features" style="margin-right:2%;">
            <h3>Notifications</h3>
            <p>Our system periodically reminds you about the bill and your consumption</p>
        </div>
        </div>`
        doWeFetch = !doWeFetch;
    }

    function displayDateTime() {

        let date = document.querySelector("#date-time");
        date.innerHTML = '';
        date.innerHTML = `${today} ${months[todayDate.getMonth()]} <i class="bi bi-dot"></i> ${format12HourTime(todayDate)}`;

    }

    function displayHome() {
        doWeFetch = !doWeFetch;
        document.querySelector("#content").innerHTML = home_data;
        assignEvents();
        displayDateTime();
        showChart();
    }


    

    function optionSelected(e) {
        let value = e.target.innerText;
        console.log(value);
        document.querySelector('#menu-chart').style.display = 'none';
        if (value == "Daily") {
            date_data = getLastSevenDays().reverse();
        }
        else if (value == "Monthly")
        {

            date_data = getLastSixMonths();
            getMonthlyArchives();
            myChart.update();

        }

        // let card = document.querySelector("#chart-holder");
        // card.removeChild(card.lastChild);


        myChart.data.labels = date_data;
        myChart.update();
        //showChart();
    }

    function toggleMenu() {
        var menu = document.querySelector('#nots');
        if (menu.style.display === 'none') {
            menu.style.display = 'block';
            let options = document.querySelectorAll(".menu li");
        } else {
            menu.style.display = 'none';
        }
    }

    function toggleCahrtMenu() {
        var menu = document.querySelector('#menu-chart');
        var icon = document.querySelector('#menu-arr');

        if (menu.style.display === 'none') {
            menu.style.display = 'block';
            let options = document.querySelectorAll("#menu-chart li");
            options.forEach(opt => opt.addEventListener("click", (e) => { optionSelected(e) }));
        } else {
            menu.style.display = 'none';
        }

        document.addEventListener("click", (e) => {
            if (!menu.contains(e.target) && !icon.contains(e.target)) {
                if (menu.style.display != "none") {
                    menu.style.display = "none";
                }
            }
        })
    }

    function assignEvents() {
        document.querySelector("#menu-arr").addEventListener("click", toggleCahrtMenu);
        document.querySelector("#notification").addEventListener("mouseover", toggleMenu);
        document.querySelector("#notification").addEventListener("mouseout", toggleMenu);
        document.querySelector("#features").addEventListener("click", displayFeatures);
        document.querySelector("#home").addEventListener("click", displayHome);

    }

    function format12HourTime(date) {
        let hours = date.getHours();
        const minutes = date.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        const minutesFormatted = minutes < 10 ? '0' + minutes : minutes;

        return hours + ':' + minutesFormatted + ' ' + ampm;
    }

});