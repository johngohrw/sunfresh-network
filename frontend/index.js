const express = require('express');
const app = express();

app.use(express.static('dashforge'));

app.get('/', (req, res) => {
    const fileName = '/template/sunfresh/dashboard.html';
    res.sendFile(fileName, options, function (err) {
        if (err) {
            next(err)
        } else {
            console.log('Sent:', fileName)
        }
    })
});

app.listen(5070, () => console.log('mojo demo app listening on port 5070!'));
