package net.cpbackend.stabilimento;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit4.SpringRunner;

import net.cpbackend.model.Stabilimento;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.http.HttpStatus.*;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class StabilimentoTest {

	@Autowired
	private TestRestTemplate restTemplate;
	
	private Stabilimento fixture;
	
	@BeforeEach
	void setUp() {
		fixture = new Stabilimento("test");
		fixture.setId(restTemplate.postForEntity("/officina/stabilimenti", fixture, Stabilimento.class).getBody().getId());
		
		if (fixture.getId() == null) throw new RuntimeException("Failed to initialize the fixture");
	}
	
	@AfterEach
	void tearDown() {
		restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.DELETE,
				null, Stabilimento.class, fixture.getId());
	}

	@Test
	void findById() {
		ResponseEntity<Stabilimento> response = restTemplate.getForEntity("/officina/stabilimenti/{id}",
				Stabilimento.class, fixture.getId());

		assertEquals(OK.value(), response.getStatusCode().value());
	}

	@Test
	void updateStabilimento() {
		fixture.setNome("test update");

		ResponseEntity<Stabilimento> response = restTemplate.exchange("/officina/stabilimenti/{id}", HttpMethod.PUT,
				new HttpEntity<>(fixture), Stabilimento.class, fixture.getId());

		assertEquals(OK.value(), response.getStatusCode().value());
		assertEquals(response.getBody().getId(), fixture.getId());
		assertEquals(response.getBody().getNome(), fixture.getNome());
	}
}