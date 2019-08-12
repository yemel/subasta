import { CountUp } from './countUp.min.js';

window.onload = function() {
    var countUp = new CountUp('#total', 2000);
    countUp.start();
}