$('document').ready(function() {
	var url = '/repos',
		h = 700,
		w = 1500;
	var svg = d3.select('body').append('svg');
	svg.attr('height', h).attr('width', w);
	var radiusScale = d3.scale.sqrt().range([1, 140]);

	function charge(d) {
		return radiusScale(d.value) * radiusScale(d.value) * -0.15;
	}

	var force = d3.layout.force()
		.gravity(0.1)
		.distance(5)
		.charge(charge)
		.size([w, h])
		.alpha(0.3);

	d3.json(url, function(error, data) {
		var maxValue = d3.max(data, function(d) {
			return d.value;
		});
		var g = svg.append('g').attr('transform', 'translate(-5, 20)');
		var circles = g.selectAll('circle')
			.data(data)
			.enter()
			.append('circle')
			.attr('fill', 'black');

		var tip = d3.tip()
			.attr('class', 'd3-tip')
			.offset([-10, 0])
			.html(function(d) {
				return "<strong>Language:</strong> " + d.language + "</span>" +
					"<br /><br /><strong>Value:</strong> " + ((d.value / maxValue) * 100).toFixed(2) + '%';
			});

		svg.call(tip);
		force.nodes(data);
		radiusScale.domain([1, maxValue])

		force.on("tick", function() {
			force.alpha(0.1);
			circles
				.attr("cx", function(d) {
					return d.x
				})
				.attr("cy", function(d) {
					return d.y
				})
				.attr("r", function(d) {
					return radiusScale(d.value);
				})
				.attr('fill', 'rgb(138, 137, 166)')
				.on('mouseover', tip.show)
				.on('mouseout', tip.hide)
				.call(force.drag);
		});

		force.start();
	});
});