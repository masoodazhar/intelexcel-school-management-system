(function ($) {
    "use strict";
    var chart_data = document.getElementById('chart_data').innerText;
    var amCharts = {
        initialize: function () {
            this.combinedBullet();
        },
        combinedBullet: function () {
            am4core.ready(function () {
                // Themes begin
                am4core.useTheme(am4themes_animated);
                // Themes end

                // Create chart instance
                var chart = am4core.create("multipleValue", am4charts.XYChart);
                
                // const mapper = new Map([['1', 'a'], ['2', 'b']]);
             
                var data = jQuery.parseJSON(chart_data)
               
                // Add data
                setTimeout(function(){
                    chart.data = data;
                    document.getElementById('chart_loader').style.display='none';
                }, 5000)
                
                // Create axes
                var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
                //dateAxis.renderer.grid.template.location = 0;
                //dateAxis.renderer.minGridDistance = 30;

                var valueAxis1 = chart.yAxes.push(new am4charts.ValueAxis());
                valueAxis1.title.text = "Months";

                var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
                valueAxis2.title.text = "Market Days";
                valueAxis2.renderer.opposite = true;
                valueAxis2.renderer.grid.template.disabled = true;

                // Create series
                var series1 = chart.series.push(new am4charts.ColumnSeries());
                series1.dataFields.valueY = "un_paid_amount";
                series1.dataFields.dateX = "date";
                series1.yAxis = valueAxis1;
                series1.name = "Monthly Unpaid Fee";
                series1.tooltipText = "{name}\n[bold font-size: 20]Rs. {valueY}[/]";
                series1.fill = chart.colors.getIndex(0);
                series1.strokeWidth = 0;
                series1.clustered = false;
                series1.columns.template.width = am4core.percent(40);

                var series2 = chart.series.push(new am4charts.ColumnSeries());
                series2.dataFields.valueY = "paid_amount";
                series2.dataFields.dateX = "date";
                series2.yAxis = valueAxis1;
                series2.name = "Monthly Paid Fee";
                series2.tooltipText = "{name}\n[bold font-size: 20]Rs. {valueY}[/]";
                series2.fill = chart.colors.getIndex(0).lighten(0.5);
                series2.strokeWidth = 0;
                series2.clustered = false;
                series2.toBack();

                // var series3 = chart.series.push(new am4charts.LineSeries());
                // series3.dataFields.valueY = "vouchers";
                // series3.dataFields.dateX = "date";
                // series3.name = "Monthly Unpaid Voucher";
                // series3.strokeWidth = 2;
                // series3.tensionX = 0.7;
                // series3.yAxis = valueAxis2;
                // series3.tooltipText = "{name}\n[bold font-size: 20]{valueY}[/]";

                // var bullet3 = series3.bullets.push(new am4charts.CircleBullet());
                // bullet3.circle.radius = 3;
                // bullet3.circle.strokeWidth = 2;
                // bullet3.circle.fill = am4core.color("#fff");

                // var series4 = chart.series.push(new am4charts.LineSeries());
                // series4.dataFields.valueY = "market2";
                // series4.dataFields.dateX = "date";
                // series4.name = "Yearly Unpaid Vouchers";
                // series4.strokeWidth = 2;
                // series4.tensionX = 0.7;
                // series4.yAxis = valueAxis2;
                // series4.tooltipText = "{name}\n[bold font-size: 20]{valueY}[/]";
                // series4.stroke = chart.colors.getIndex(0).lighten(0.5);
                // series4.strokeDasharray = "3,3";

                // var bullet4 = series4.bullets.push(new am4charts.CircleBullet());
                // bullet4.circle.radius = 3;
                // bullet4.circle.strokeWidth = 2;
                // bullet4.circle.fill = am4core.color("#fff");

                // Add cursor
                chart.cursor = new am4charts.XYCursor();

                // Add legend
                chart.legend = new am4charts.Legend();
                chart.legend.position = "top";

                // Add scrollbar
                chart.scrollbarX = new am4charts.XYChartScrollbar();
                chart.scrollbarX.series.push(series1);
                chart.scrollbarX.series.push(series3);
                chart.scrollbarX.parent = chart.bottomAxesContainer;

            }); // end am4core.ready()

        }
    };
    // Initialize
    $(document).ready(function () {
        "use strict"; // Start of use strict
        amCharts.initialize();
    });

}(jQuery));