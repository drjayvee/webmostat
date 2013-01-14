YUI.add('webmostat', function(Y) {
    function Webmostat(config) {
        Webmostat.superclass.constructor.apply(this, arguments);
    }
    Webmostat.NAME = 'webmostat';
    Webmostat.ATTRS = {
        tabView:   {},
        tempSeries: {
            writeOnce:  'initOnly'
        }
    };

    Y.extend(Webmostat, Y.Base, {
        run: function () {
            var tv = new Y.TabView({srcNode: '#tabs'});

            this.set('tabView', tv);
            tv.render();

            this._initControl();
            this._initTemperature();
            this._initSchedule();
        },

        _initControl: function () {
            Y.all('#control .yui3-button').each(function (input) {
                var pin = input.getAttribute('data-pin');

                new Y.ToggleButton({srcNode: input})
                    .render()
                    .after('pressedChange', function () {
                        this.set('label', this.get('disabled') ? 'Enable' : 'Disable');
                        Y.io( '/ajax/setThermostat', {
                            method: 'POST',
                            data: {
                                pin:        pin,
                                active:     Y.JSON.stringify(this.get('pressed'))
                            },
                            on: {
                                failure: function (ioId, res) {
                                    alert('Could not toggle thermostat: ' + res.responseText);
                                    this.set('disabled', true)
                                        .set('label', 'Broken!');
                                }
                            },
                            context: this
                        } );
                    });
            });
        },

        _initTemperature: function () {
            var chart,
                times = [],
                temps = [];

            this.get('tempSeries').forEach(function (temp){
                times.push(temp[0]);
                temps.push(temp[1]);
            });

            chart = new Y.Chart({
                dataProvider:   [times, temps],
                type:           'spline',
                categoryType:   'time'
            });

            chart.getAxisByKey('values')
                .set('alwaysShowZero', false);

            chart.getAxisByKey('category')
                .set('labelFunction', function (ts){
                    var d = new Date(ts * 1000);
                    return d.getHours() + ':' + d.getMinutes();
                })
                .set('styles', {majorUnit: {count: 6}});

            this.get('tabView').item(1).after('selectedChange', function (e) {
                chart.render('#tempChart');
            });
        },

        _initSchedule: function () {}
    });

    Y.Webmostat = Webmostat;
}, '0.1337', {requires: ['base', 'button', 'charts', 'io', 'json-stringify', 'tabview']} );
