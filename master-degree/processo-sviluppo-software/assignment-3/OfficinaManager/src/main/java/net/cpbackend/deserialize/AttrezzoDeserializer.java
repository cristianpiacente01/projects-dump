package net.cpbackend.deserialize;

import java.io.IOException;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import net.cpbackend.model.Attrezzo;
import net.cpbackend.model.Motosega;
import net.cpbackend.model.Trapano;

public class AttrezzoDeserializer extends JsonDeserializer<Attrezzo> {

	@Override
	public Attrezzo deserialize(JsonParser jp, DeserializationContext ctxt)
			throws IOException, JsonProcessingException {
		ObjectMapper mapper = (ObjectMapper) jp.getCodec();

		String json = jp.readValueAsTree().toString(); // json string

		String tipo = mapper.readTree(json).path("tipo").asText(); // tipo in the json

		// throw an exception if the type is not valid
		
		if (!tipo.equals("M") && !tipo.equals("T")) {
			throw JsonMappingException.from(ctxt, "Invalid attrezzo type");
		}
		
		// deserialize a motosega or trapano depending on the type

		if (tipo.charAt(0) == 'M') {
			return mapper.readValue(json, Motosega.class);
		} else { // 'T'
			return mapper.readValue(json, Trapano.class);
		}
	}
}